# internal imports
import windupbox.config as config

# configure logging
from windupbox.logger import logger
import logging as log


def setup_logging(arguments, commandline):
    loglevel_console = None
    if arguments.loglevelconsole:
        if arguments.loglevelconsole in config.ABBREV_DEBUG:
            loglevel_console = log.DEBUG
        elif arguments.loglevelconsole in config.ABBREV_INFO:
            loglevel_console = log.INFO
        elif arguments.loglevelconsole in config.ABBREV_WARNING:
            loglevel_console = log.WARNING
        elif arguments.loglevelconsole in config.ABBREV_ERROR:
            loglevel_console = log.ERROR
        elif arguments.loglevelconsole in config.ABBREV_CRITICAL:
            loglevel_console = log.CRITICAL
    loglevel_file = None
    if arguments.loglevelfile:
        if arguments.loglevelfile in config.ABBREV_DEBUG:
            loglevel_file = log.DEBUG
        elif arguments.loglevelfile in config.ABBREV_INFO:
            loglevel_file = log.INFO
        elif arguments.loglevelfile in config.ABBREV_WARNING:
            loglevel_file = log.WARNING
        elif arguments.loglevelfile in config.ABBREV_ERROR:
            loglevel_file = log.ERROR
        elif arguments.loglevelfile in config.ABBREV_CRITICAL:
            loglevel_file = log.CRITICAL
    details = arguments.logdetailsconsole
    logfile = None
    if arguments.logfile:
        logfile = arguments.logfile

    if logfile:
        with open(logfile, mode='w') as f:
            f.write(f'{config.NAME} in version {config.VERSION} with command {" ".join(commandline)}\n')

    logger.setup_logger(loglevel_console=loglevel_console, logfile=logfile, loglevel_file=loglevel_file,
                        console_details=details)

    log.info(f'running command: {" ".join(commandline)}')
