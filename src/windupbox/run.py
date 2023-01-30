# external imports
import argparse
import sys
import time
import shutil
from pathlib import Path
import pkg_resources

# internal imports
from windupbox.setup_logging import setup_logging
from windupbox.helperFunctions.argparse.formatter import SmartFormatter
from windupbox.cli.os import os_list, os_add, os_remove, os_set_tested, os_update, os_download
from windupbox.cli.boxcreate import boxcreate
from windupbox.cli.showversion import show_version
from windupbox.osinfo.constants import DATABASE_FILE_OSINFO


def run():
    # todo: update help messages
    start_time = time.time()

    parser = argparse.ArgumentParser()
    # parser_tree = NodeHelpMessage('root_parser', parser=parser)

    parser.add_argument('-v', '--version', action='store_true', help='display program version')
    parser.add_argument('--logfile')
    parser.add_argument('--loglevelfile')
    parser.add_argument('--loglevelconsole')
    parser.add_argument('--logdetailsconsole', type=bool, default=False)
    parser.set_defaults(func=lambda args: show_version(args, parser))

    subparsers = parser.add_subparsers(dest='subcommand')

    # subcommand boxcreate
    parser_boxcreate = subparsers.add_parser('boxcreate',
                                             help=f'create automated a vagrant box that can be used for forensic tool ...',
                                             formatter_class=SmartFormatter)
    parser_boxcreate.add_argument('-d', '--boxdirectory', type=str,
                                  help=f'directory that will be used to create the box (box will be placed in the box directory)')
    # parser_boxcreate.add_argument('-av', '--addtovagrant', type=str,
    #                          help=f'add box to vagrant with a provided name (and add minimal Vagrantfile to output)')
    parser_boxcreate.add_argument('-ch', '--choco', action='store_true',
                                  help='install chocolatey')
    parser_boxcreate.add_argument('-chp', '--choco-packages', type=str,
                                  help='install provided packages with choco (and automatically install chocolatey)')
    parser_boxcreate.add_argument('-ps', '--powershell-scripts', type=str, default='',
                                  help='run provided powershell scripts (provide a directory or a set of files)')
    parser_boxcreate.add_argument('-ssh', '--ssh', action='store_true',
                                  help='install OpenSSH Server and set up so that it can be used be vagrant as the communicator')
    parser_boxcreate.add_argument('-iso', '--iso', type=str,
                                  help='path of an windows iso file (will skip the download process)')
    parser_boxcreate.add_argument('-key', '--windows-key', type=str,
                                  help='windows key to be used during installation')
    parser_boxcreate.add_argument('-bcp', '--bcp47', type=str,
                                  help='specify the bcp47 code used for the language for keyboard layout and installation - to see a full list look here https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oe376/6c085406-a698-4e12-9d4d-c3b0ee3dbc4a')
    parser_boxcreate.add_argument('--disable-cleanup', action='store_true',
                                  help='disable cleanup after packer build process to keep the used scripts and the packerfile')
    # parser_boxcreate.add_argument('-l', '--list', help='list all available os')
    # parser_boxcreate.add_argument('-c', '--communicator', )

    help_message_osinfo = "R|information about the os seperated by comma\n\n" \
                          "Windows: \n" \
                          "\t(windows_version, version, edition, language, architecture) \n" \
                          "\te.g.: ('Windows 10', '21H1', 'Pro', 'English', 'x64')"
    parser_boxcreate.add_argument('osinfo', help=help_message_osinfo)
    parser_boxcreate.set_defaults(func=boxcreate)

    # subcommand os
    parser_os = subparsers.add_parser('os', help=f'subparser to show and modify the available os options')
    parser_os.set_defaults(func=parser_os.print_help)
    subparsers_os = parser_os.add_subparsers()

    # subcommand os/list
    parser_oslist = subparsers_os.add_parser('list', help='list available os (from os_info database)',
                                             formatter_class=SmartFormatter)
    parser_oslist.add_argument('-a', '--show-all', help='list all available os', action='store_true')
    parser_oslist_selectcolumns_help = 'R|show only certain columns described by their name and split by a comma (,' \
                                       ') \navailable columns: windows_version, version, edition, language, ' \
                                       'architecture, build (optional), release (optional), tested \n(e.g. -s \'windows_version,edition\')'
    parser_oslist.add_argument('-s', '--select-columns', help=parser_oslist_selectcolumns_help)
    parser_oslist_filter_help = 'R|filter the results by using key value pairs (key=value) seperated by comma (,' \
                                ') \navailable columns: windows_version, version, edition, language, ' \
                                'architecture, build (optional), release (optional), tested \n(e.g. -f \'windows_version=Windows 10,edition=Pro\')'
    parser_oslist.add_argument('-f', '--filter', help=parser_oslist_filter_help)
    parser_oslist.add_argument('-fi', '--format_as_input', help=f'format such that in can be copied line per line for e.g the os download subcommand', action='store_true')
    parser_oslist.set_defaults(func=lambda args: os_list(args, parser_oslist))

    windows_info_help_message = 'R|windows info in key value style (key=value) seperated ' \
                                'by comma (,)\nnecessarry columns: windows_version, ' \
                                'version, edition, language,architecture\n(' \
                                'e.g.\'windows_version=WindowsTest,version=1,' \
                                'edition=Home,language=English,architecture=x64\')'
    # subcommand os/add
    parser_osadd = subparsers_os.add_parser('add', help='add os information to os options (to os_info database)',
                                            formatter_class=SmartFormatter)
    parser_osadd.add_argument('windows_info', type=str, help=windows_info_help_message)
    parser_osadd.set_defaults(func=os_add)

    # subcommand os/remove
    parser_osremove = subparsers_os.add_parser('remove',
                                             help='remove os information from os options (from os_info database)', formatter_class=SmartFormatter)
    parser_osremove.add_argument('windows_info', type=str, help=windows_info_help_message)
    parser_osremove.set_defaults(func=os_remove)

    parser_osupdate = subparsers_os.add_parser('update',  help='update the database by scraping the microsoft website for available isos')
    parser_osupdate.set_defaults(func=os_update)

    # # subcommand recover
    # parser_recover = subparsers_os.add_parser('recover')
    # parser_recover.set_defaults(func=os_recover)

    # subcommand set tested
    parser_settested = subparsers_os.add_parser('set_tested', help='set tested attribute of os information to True', formatter_class=SmartFormatter)
    parser_settested.add_argument('windows_info', type=str, help=windows_info_help_message)
    parser_settested.set_defaults(func=os_set_tested)

    # subcommand download
    parser_download = subparsers_os.add_parser('download',
                                             help=f'download an specific windows iso',
                                             formatter_class=SmartFormatter)
    parser_download.add_argument('osinfo', help=help_message_osinfo)
    parser_download.add_argument('-d', '--output-directory', help='filepath of downloaded file')
    parser_download.add_argument('-bcp', '--bcp47', type=str,
                                  help='specify the bcp47 code used for the language for keyboard layout and installation - to see a full list look here https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oe376/6c085406-a698-4e12-9d4d-c3b0ee3dbc4a')
    parser_download.set_defaults(func=os_download)

    # parse args
    args = parser.parse_args()

    setup_logging(args, sys.argv)

    # configure logging
    import logging
    log = logging.getLogger(__name__)

    # copy database if not existing
    if not DATABASE_FILE_OSINFO.is_file():
        # todo: exchange by requesting the database from github
        local_db = Path(pkg_resources.resource_filename('windupbox', '/data/osinfo.db'))
        shutil.copy(local_db.as_posix(), DATABASE_FILE_OSINFO.as_posix())
        log.info(f'database got added to the config directory ({DATABASE_FILE_OSINFO})')
        print(f'database got added to the config directory ({DATABASE_FILE_OSINFO})')

    # run function
    args.func(args)

    log.debug(f"---  Runtime {(time.time() - start_time) / 60} minutes ---")
    logging.shutdown()
