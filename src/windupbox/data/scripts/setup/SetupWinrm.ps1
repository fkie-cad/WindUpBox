# Enable Winrm and create Firewall Rule automatically
# The Enable-PSRemoting cmdlet performs the following operations:
#    Runs the Set-WSManQuickConfig cmdlet, which performs the following tasks:
#        Starts the WinRM service.
#        Sets the startup type on the WinRM service to Automatic.
#        Creates a listener to accept requests on any IP address.
#        Enables a firewall exception for WS-Management communications.
#        Creates the simple and long name session endpoint configurations if needed.
#        Enables all session configurations.
#        Changes the security descriptor of all session configurations to allow remote access.
#    Restarts the WinRM service to make the preceding changes effective.

Enable-PSRemoting -SkipNetworkProfileCheck -Force