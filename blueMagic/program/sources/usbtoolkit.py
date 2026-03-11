# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'usbtoolkit.py'
# Bytecode version: 3.13.0rc3 (3571)

import os
import sys
import subprocess
import shutil
from colorama import init, Fore, Style
from time import sleep

init()

tools = {
    1: {'name': 'Auto-Executor', 'lnk_name': 'Private_Documents.lnk', 'leurre_dir': 'Documents'},
    2: {'name': 'Data Exfiltrator', 'lnk_name': 'Backup_Files.lnk', 'leurre_dir': 'Data'},
    3: {'name': 'Registry Injector', 'lnk_name': 'System_Config.lnk', 'leurre_dir': 'Config'},
    4: {'name': 'Fake Format', 'lnk_name': 'Repair_USB.lnk', 'leurre_dir': 'Repair'}
}

def print_cyan(text):
    print(f'{Fore.LIGHTCYAN_EX}{text}{Style.RESET_ALL}')

def input_cyan(prompt):
    return input(f'{Fore.LIGHTCYAN_EX}{prompt}{Style.RESET_ALL}')

def loading_bar(message, duration=2, steps=20):
    print_cyan(f'[*] {message}...')
    for i in range(steps + 1):
        progress = int(i / steps * 100)
        bar = '\u2588' * (i // 2) + ' ' * ((steps - i) // 2)
        sys.stdout.write(f'\r[{bar}] {progress}%')
        sys.stdout.flush()
        sleep(duration / steps)
    print('\r[ OK ]                                         ')

def validate_usb_path(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        return False
    try:
        test_file = os.path.join(path, '.test_write')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except PermissionError:
        return False

def configure_usb(tool_id, usb_path, exe_name=None):
    tool = tools[tool_id]
    tool_dir = os.path.join(usb_path, tool['leurre_dir'])
    try:
        os.makedirs(tool_dir, exist_ok=True)
    except PermissionError:
        print_cyan(f'[-] ERROR: Permission denied creating {tool_dir}')
        return False
    
    readme_path = os.path.join(tool_dir, 'readme.txt')
    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f'Click the shortcut to access {tool["leurre_dir"]}!')
    except PermissionError:
        print_cyan('[-] ERROR: Permission denied writing readme')
        return False
    
    print_cyan(f'[*] USB configured with {tool["name"]} at {tool_dir}')
    return True

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_cyan('======================================================================')
    print_cyan('               USB ToolKit v1.8')
    print_cyan('======================================================================')
    print()
    print_cyan('Select USB tool:')
    print_cyan('[1] USB Auto-Executor    : Run script on click')
    print_cyan('[2] USB Data Exfiltrator : Steal files silently')
    print_cyan('[3] USB Registry Injector: Persist on boot')
    print_cyan('[4] USB Fake Format      : Fake corruption trick')
    
    try:
        tool_choice = int(input_cyan('Enter tool number (1-4): '))
        if tool_choice not in range(1, 5):
            print_cyan('[!] Invalid tool choice. Exiting.')
            sys.exit(1)
    except ValueError:
        print_cyan('[!] Invalid input. Exiting.')
        sys.exit(1)
    
    usb_path = input_cyan('Enter USB drive path (e.g., E:\\): ').strip()
    if not validate_usb_path(usb_path):
        print_cyan('[!] Invalid USB path or no write access.')
        sys.exit(1)
    
    exe_name = None
    if tool_choice != 2:
        exe_name = input_cyan('Enter exe name (or press Enter to skip): ').strip() or None
    
    loading_bar('Configuring USB key', duration=2)
    if configure_usb(tool_choice, usb_path, exe_name):
        print_cyan(f'[+] USB ready with {tools[tool_choice]["name"]}')
    else:
        print_cyan('[!] USB configuration failed.')
    
    loading_bar('Operation Complete', duration=1)

if __name__ == '__main__':
    main()
