import winreg
import subprocess
import ctypes
registry_entries = [
    (r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "PlatformSupportMiracast", 0),
    (r"SYSTEM\CurrentControlSet\Services\nvlddmkm\FTS", "EnableRID61684", 1),
    (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "SystemResponsiveness", 0),
    (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "NetworkThrottlingIndex", "ffffffff"),
    (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "GPU Priority", "8"),
    (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "SFIO Priority", "High"),
    (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "Scheduling Category", "High"),
    (r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{2e1f0e2d-7529-4ca9-a2d2-e640bf7e04f8}", "TcpAckFrequency", "1"),
    (r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{2e1f0e2d-7529-4ca9-a2d2-e640bf7e04f8}", "TcpAckFrequency", "1"),
    (r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{2e1f0e2d-7529-4ca9-a2d2-e640bf7e04f8}", "TCPNoDelay", "1"),
    (r"SYSTEM\CurrentControlSet\Control\Power\PowerThrottling", "PowerThrottlingOff", "1"),
    (r"System\GameConfigStore", "GameDVR_Enabled", "0"),
    (r"Control Panel\Desktop", "MenuShowDelay", "0"),
    (r"SYSTEM\CurrentControlSet\Services\AFD\Parameters", "MenuShowDelay", "0"),
    (r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "MaxNumRssCpus", "4"),
    (r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", "MaxNumRssCpus", "4"),
    (r"SYSTEM\CurrentControlSet\Services\mouhid\Parameters", "UseOnlyMice", "1"),
    (r"SYSTEM\CurrentControlSet\Services\mouhid\Parameters", "TreatAbsoluteAsRelative", "0"),
    (r"SYSTEM\CurrentControlSet\Services\mouhid\Parameters", "TreatAbsolutePointerAsAbsolute", "1"),
    (r"SYSTEM\CurrentControlSet\Services\kbdclass\Parameters", "MaximumPortsServiced", "1"),
    (r"SYSTEM\CurrentControlSet\Services\kbdclass\Parameters", "SendOutputToAllPorts", "0"),
    (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\VALORANT-Win64-Shipping.exe\PerfOptions", "CpuPriorityClass", "3")
]

def set_registry_value(key_path, name, value):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ if isinstance(value, str) else winreg.REG_DWORD, value)
        winreg.CloseKey(key)
        print(f"Successfully set registry value: HKEY_LOCAL_MACHINE\\{key_path}\\{name}")
    except Exception as e:
        print(f"Error: {e}")

for entry in registry_entries:
    key_path, name, value = entry
    set_registry_value(key_path, name, value)

# Function to display a pop-up message box



batch_script = r"""
@echo off
for /f %%i in ('wmic path Win32_VideoController get PNPDeviceID^| findstr /L "PCI\VEN_"') do (
    for /f "tokens=3" %%a in ('reg query "HKLM\SYSTEM\ControlSet001\Enum\%%i" /v "Driver"') do (
        for /f %%i in ('echo %%a ^| findstr "{"') do (
            Reg.exe add "HKLM\SYSTEM\CurrentControlSet\Control\Class\%%i" /v "RMHdcpKeyglobZero" /t REG_DWORD /d "1" /f > nul 2>&1
        )
    )
)
"""

try:
    # Run the batch script using subprocess
    subprocess.run(batch_script, shell=True, check=True)
    print("Batch script executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running the batch script: {e}")


batch_code = r'''
@echo off
setlocal enableextensions

sc config Winmgmt start= demand >nul 2>&1
sc start Winmgmt >nul 2>&1
for /f %%i in ('wmic path win32_networkadapter get GUID ^| findstr "{"') do reg add "HKLM\System\CurrentControlSet\services\Tcpip\Parameters\Interfaces\%%i" /v "TcpAckFrequency" /t REG_DWORD /d "1" /f >nul 2>&1
for /f %%i in ('wmic path win32_networkadapter get GUID ^| findstr "{"') do reg add "HKLM\System\CurrentControlSet\services\Tcpip\Parameters\Interfaces\%%i" /v "TcpDelAckTicks" /t REG_DWORD /d "0" /f >nul 2>&1
for /f %%i in ('wmic path win32_networkadapter get GUID ^| findstr "{"') do reg add "HKLM\System\CurrentControlSet\services\Tcpip\Parameters\Interfaces\%%i" /v "TCPNoDelay" /t REG_DWORD /d "1" /f >nul 2>&1

:: netsh winsock set autotuning on >nul 2>&1

netsh int ip set global neighborcachelimit=4096 >nul 2>&1
netsh int ip set global routecachelimit=4096 >nul 2>&1
netsh int ip set global sourceroutingbehavior=drop >nul 2>&1
:: Security concerns
netsh int ip set global taskoffload=enabled >nul 2>&1
netsh int ip set global dhcpmediasense=disabled >nul 2>&1
netsh int ip set global mediasenseeventlog=disabled >nul 2>&1
netsh int ip set global mldlevel=none >nul 2>&1
netsh int ip set global icmpredirects= disabled >nul 2>&1
:: netsh int ip set global randomizeidentifiers= disabled >nul 2>&1 less secure
:: Disable ICMP Redirects for security
netsh int tcp set global chimney=enabled >nul 2>&1
netsh int tcp set global dca=enabled >nul 2>&1
netsh int tcp set global netdma=disabled >nul 2>&1
netsh int tcp set global rsc=disabled >nul 2>&1
netsh int tcp set global maxsynretransmissions=2 >nul 2>&1
netsh int tcp set global timestamps=disabled >nul 2>&1
netsh int tcp set global ecncapability=disabled >nul 2>&1
:: netsh int tcp set global congestionprovider=ctcp >nul 2>&1

netsh interface teredo set state disabled >nul 2>&1
netsh int isatap set state disable >nul 2>&1

for /f "tokens=1" %%i in ('netsh int ip show interfaces ^| findstr [0-9]') do set INTERFACE=%%i >nul 2>&1
netsh int ip set interface %INTERFACE% basereachable=3600000 dadtransmits=0 otherstateful=disabled routerdiscovery=disabled store=persistent >nul 2>&1

:: netsh int tcp set global initialRto=2000 >nul 2>&1

netsh int tcp set heuristics disabled >nul 2>&1
netsh int tcp set heuristics wsh=disabled >nul 2>&1

netsh int tcp set security mpp=disabled >nul 2>&1
netsh int tcp set security profiles=disabled >nul 2>&1

netsh int ipv4 set dynamicport tcp start=1025 num=64511 >nul 2>&1
netsh int ipv4 set dynamicport udp start=1025 num=64511 >nul 2>&1

powershell Set-NetTCPSetting -SettingName "*" -ForceWS Disabled >nul 2>&1
'''

try:
    # Run the batch code using subprocess
    subprocess.run(batch_code, shell=True, check=True)
    print("Batch script executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running the batch script: {e}")




message = "completed if your pc is on wifi and is no longer connecting please input 'error'"


# Function to display a pop-up message box
def display_message_box(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Message", 0x40 | 0x1)

try:
    # Display the message using the custom function
    display_message_box(message)
except Exception as e:
    print(f"Error occurred while displaying the message: {e}")



user_input = input("Enter:   ")

if user_input == "error":
    batch_code = r'''
@echo off
echo Resetting Network
ipconfig /flushdns
ipconfig /release
ipconfig /renew
pause
'''

    try:
        subprocess.run(batch_code, shell=True, check=True)
        print("Batch script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the batch script: {e}")
else:
    print("pc optimised closing now")
