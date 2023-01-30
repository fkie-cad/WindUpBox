# external imports
from pathlib import Path

# internal imports
from windupbox.boxcreator.provided.windows import WindowsBoxCreator
from windupbox.helperFunctions.strings.strtolist import str_to_list
from windupbox.helperFunctions.input.yesnoinput import yesnoinput
from windupbox.osinfo.windowsinfo import WindowsInfo
from windupbox.boxcreator.selector import select_boxcreator_by_windows_info
from windupbox.helperFunctions.strings.replace import replace_multiple_strings
from ._parse_parameters import get_windowsinfo_for_creation, determine_bcp47

# configure logging
import logging
log = logging.getLogger(__name__)


def _setup_powershell_scripts(powershell_scripts: str, boxcreator: WindowsBoxCreator):
    if powershell_scripts:
        scripts = str_to_list(powershell_scripts, delim=[','], start_chars=['(', '['], end_chars=[')', ']'])
        existing_scripts = []
        for script in scripts:
            if not Path(script).is_file():
                message = f'provided powershell script with path {script} does not exist'
                log.error(message)
                print(message)
                result = yesnoinput('Do you still want to continue creating the box without the script?', tries=3)
                if result == 0:
                    log.info(f'box creation did not start due to a provided powershell script that doesn\'t exist')
                    return
                elif result == 1:
                    log.warning(f'box creation will continue even though an provided powershell script does not exist')
                else:
                    log.error(
                        f'No valid to the question whether to continue or stop the box was provided. Therefore the box will be not created. Please try again.')
                    return
            else:
                existing_scripts.append(Path(script))
        boxcreator.add_powershell_provisioners(existing_scripts)


def _setup_chocolatey_packages(choco: str, choco_packages: str, boxcreator: WindowsBoxCreator):
    if choco or choco_packages:
        packages = []
        if choco_packages:
            packages = str_to_list(choco_packages, delim=[','], start_chars=['(', '['], end_chars=[')', ']'])
        boxcreator.add_chocolatey_provisioner(packages=packages)


def _setup_ssh(ssh: bool, boxcreator: WindowsBoxCreator):
    if ssh:
        boxcreator.add_provisioner_setup_ssh()


def _add_iso_to_boxcreation(iso: str, boxcreator: WindowsBoxCreator) -> bool:
    if iso:
        iso_file = Path(iso)
        if not iso_file.is_file():
            message = f'the provided image with path {iso_file} does not exist'
            log.error(message)
            print(message)
            result = yesnoinput(
                'Do you still want to continue creating the box with downloading the windows image instead?', tries=3)
            if result == 0:
                log.info(f'box creation did not start because the provided image doesnt exist')
                return False
            elif result == 1:
                log.warning(f'box creation will continue with downloading the windows image')
            else:
                log.error(
                    f'No valid to the question whether to continue or stop the box was provided. Therefore the box will be not created. Please try again.')
                return False
        boxcreator.set_image(iso_file)
    return True


def boxcreate(arguments):
    """
        cli function to create a box image
    """
    boxcreator = None
    try:
        windows_info = get_windowsinfo_for_creation(arguments.osinfo)
        if not windows_info:
            log.error(f'provided windows information is missing key -> please provide all necessary attributes')
            return

        bcp47 = determine_bcp47(arguments, windows_info)
        if not bcp47:
            log.fatal('no bcp47 code could be found')
            return
        windows_info.set_bcp47(bcp47)

        BoxcreatorClass = select_boxcreator_by_windows_info(windows_info)
        if not BoxcreatorClass:
            print(f'no Boxcreator for the provided windows info {windows_info} was found -> feel free to create and share one')
            log.error(f'no Boxcreator for the provided windows info {windows_info} exists')
            return

        boxdirectory = arguments.boxdirectory
        if not boxdirectory:
            forbidden_chars = ['.', ' ', '-']
            windows_version_filename = replace_multiple_strings(windows_info.windows_version, forbidden_chars, '')
            edition_filename = replace_multiple_strings(windows_info.edition, forbidden_chars, '')
            version_filename = replace_multiple_strings(windows_info.version, forbidden_chars, '')
            language_filename = replace_multiple_strings(windows_info.language, forbidden_chars, '')
            boxdirectory = f'{windows_version_filename}_{edition_filename}_{version_filename}_{language_filename}'
        boxcreator = BoxcreatorClass(Path(boxdirectory).absolute(), windows_info)

        if arguments.windows_key:
            boxcreator.set_product_key(arguments.windows_key)
        # if arguments.addtovagrant:
        #     boxcreator.add_box_to_vargant(arguments.addtovagrant)

        _setup_chocolatey_packages(arguments.choco, arguments.choco_packages, boxcreator)
        _setup_powershell_scripts(arguments.powershell_scripts, boxcreator)
        _setup_ssh(arguments.ssh, boxcreator)
        if not _add_iso_to_boxcreation(arguments.iso, boxcreator):
            return

        if not arguments.disable_cleanup:
            boxcreator.cleanup_active = False

        boxcreator.create_box()

    except KeyboardInterrupt:
        print(f'\n\nprogram will exit due to a KeyboardInterrupt')
        log.info(f'program will exit due to a KeyboardInterrupt')
        logging.shutdown()
        log.debug(f'logging was shutdown successful')
        if not arguments.disable_cleanup:
            if boxcreator:
                boxcreator.cleanup()
                log.debug(f'cleanup after KeyboardInterrupt done')
