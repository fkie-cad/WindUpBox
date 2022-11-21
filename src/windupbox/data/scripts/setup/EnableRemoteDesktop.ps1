# Enable Remote Desktop
reg add "HKLM\System\CurrentControlSet\Control\Terminal Server" /v "fDenyTSConnections" /t REG_DWORD /d 0 /f

# Allow connections from computers running any version of Remote Desktop (less secure)
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v "UserAuthentication" /t REG_DWORD /d 0 /f


Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
Enable-NetFirewallRule -DisplayGroup "Windows Remote Management"

# Use the plaintext WinRM transport and force it to use basic authentication
winrm set winrm/config/service '@{AllowUnencrypted="true"}'