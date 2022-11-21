# internal imports
from windupbox.winautounattendAPI.synchronouscommand import SynchronousCommand

# configure logging
import logging
log = logging.getLogger(__name__)

set_execution_policy = SynchronousCommand(
    r'cmd.exe /c powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Force"',
    r'Set Execution Policy 64 Bit',
)

fix_public_network = SynchronousCommand(
    r'cmd.exe /c powershell -File A:\fixnetwork.ps1',
    r'Fix public network',
)

enable_winrm = SynchronousCommand(
    r'cmd.exe /c powershell -File A:\ConfigureRemotingForAnsible.ps1 -SkipNetworkProfileCheck -GlobalHttpFirewallAccess',
    r'Enable WinRM',
)