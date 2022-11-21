# external imports
from pathlib import Path
from subprocess import Popen, PIPE
import os

# internal imports
from windupbox.helperFunctions.strings.replace import replace_multiple_strings

# configure logging
import logging
log = logging.getLogger(__name__)


def packer_build(packerfile_path: Path, packer_path: Path = None, logfile: Path = None) -> dict:
    cwd = packerfile_path.parent.as_posix()
    if not packer_path:
        command = ['packer', 'build', packerfile_path.name]
    else:
        command = [packer_path.as_posix(), 'build', packerfile_path.name]
    log.info(f'run packer with command {" ".join(command)} (cwd {cwd}) - this can take several minutes')

    env_vars = os.environ.copy()
    if logfile:
        env_vars['PACKER_LOG'] = '1'
        env_vars['PACKER_LOG_PATH'] = logfile.as_posix()

    proc = Popen(command, stdout=PIPE, stderr=PIPE, cwd=cwd, shell=False, env=dict(env_vars))

    try:
        stdout = []
        stderr = []
        for line in proc.stdout:
            line = line.decode("utf-8", errors='ignore')
            line = replace_multiple_strings(line, ["\n", "\r"], " ")
            log.debug(line)
            stdout.append(line)
        for line in proc.stderr:
            line = line.decode("utf-8", errors='ignore')
            line = replace_multiple_strings(line, ["\n", "\r"], " ")
            log.error(line)
            stderr.append(line)
        proc.communicate()
        ret = {
            'returncode': proc.returncode,
            'stdout': stdout,
            'stderr': stderr
        }
    except KeyboardInterrupt:
        proc.kill()
        raise KeyboardInterrupt

    log.debug(f'{" ".join(command)} (cwd {cwd}) exited with returncode: {ret["returncode"]}')
    if ret['returncode'] != 0:
        log.error(f'{" ".join(command)} (cwd {cwd}) exited with an error (returncode: {ret["returncode"]})')
    else:
        log.info(f'packer ({" ".join(command)}) exited successfully.')
    return ret
