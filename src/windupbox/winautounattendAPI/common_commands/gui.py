# internal imports
from windupbox.winautounattendAPI.synchronouscommand import SynchronousCommand

# configure logging
import logging
log = logging.getLogger(__name__)


network_prompt_disable = SynchronousCommand(
    r'cmd.exe /c reg add "HKLM\System\CurrentControlSet\Control\Network\NewNetworkWindowOff"',
    r'Disable Network prompt',
)