# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: Spoofer.py
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

global spoofed  # inserted
global new_disk_serial  # inserted
global original_hwids  # inserted
import os
import sys
import random
import string
import winreg
import atexit
import signal
import subprocess
import shutil
from pathlib import Path
from colorama import init, Fore, Style
import ctypes
import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime, UTC
init()

def gradient(start_color, end_color, steps):
    """Interpolate colors between start and end."""  # inserted
    gradient_colors = []
    for i in range(steps):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * i / (steps - 1))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * i / (steps - 1))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * i / (steps - 1))
        gradient_colors.append((r, g, b))
    return gradient_colors

def print_gradient_ascii(ascii_art, start_color=(128, 0, 128), end_color=(255, 165, 0)):
    """Print ASCII art in red (ignoring gradient)."""  # inserted
    text = ascii_art.splitlines()
    for line in text:
        print(f'{Fore.RED}{line}{Style.RESET_ALL}')

def print_gradient_text(text, start_color=(128, 0, 128), end_color=(255, 165, 0)):
    """Print text in red (ignoring gradient)."""  # inserted
    print(f'{Fore.RED}{text}{Style.RESET_ALL}')
ASCII_ART = '\n _______   __                             __                                    __     __ \n|       \\ |  \\                           |  \\                                  |  \\   |  \\\n| $$$$$$$\\| $$____    ______   _______  _| $$_     ______   ______ ____        | $$   | $$\n| $$__/ $$| $$    \\  |      \\ |       \\|   $$ \\   /      \\ |      \\    \\       | $$   | $$\n| $$    $$| $$$$$$$\\  \\$$$$$$\\| $$$$$$$\\\\$$$$$$  |  $$$$$$\\| $$$$$$\\$$$$\\       \\$$\\ /  $$\n| $$$$$$$ | $$  | $$ /      $$| $$  | $$ | $$ __ | $$  | $$| $$ | $$ | $$        \\$$\\  $$ \n| $$      | $$  | $$|  $$$$$$$| $$  | $$  \\$$  $$ \\$$    $$| $$ | $$ | $$         \\$$ $$  \n| $$      | $$  | $$ \\$$    $$| $$  | $$  \\$$  $$ \\$$    $$| $$ | $$ | $$          \\$$$   \n \\$$       \\$$   \\$$  \\$$$$$$$ \\$$   \\$$   \\$$$$   \\$$$$$$  \\$$  \\$$  \\$$           \\$    \n'
original_hwids = { }
new_disk_serial = None
spoofed = False

def set_seed():
    """Set a random seed for reproducible HWID generation."""
    global SEED
    SEED = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
    random.seed(SEED)
    print_gradient_text(f'[*] Seeding system initialized with seed: {SEED}')

def generate_cpu_id():
    """Generate a realistic CPU ID."""  # inserted
    prefixes = ['AMD Ryzen 7 5800X', 'Intel Core i9-12900K', 'AMD Ryzen 5 5600X']
    return random.choice(prefixes)

def generate_gpu_id():
    """Generate a realistic GPU ID."""  # inserted
    models = ['NVIDIA RTX 3080', 'AMD RX 6800', 'Intel Arc A770']
    return random.choice(models)

def generate_disk_serial():
    """Generate a realistic disk serial number."""  # inserted
    manufacturers = ['WD', 'ST', 'SAMSUNG']
    prefix = random.choice(manufacturers)
    serial = ''.join((random.choice(string.ascii_uppercase + string.digits) for _ in range(8)))
    return f'{prefix}{serial}'

def get_current_cpu_id():
    """Get current CPU ID from registry."""  # inserted
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0', 0, winreg.KEY_READ)
        cpu_id = winreg.QueryValueEx(key, 'Identifier')[0]
        winreg.CloseKey(key)
        return cpu_id if cpu_id else None
    except:
        return None

def get_current_gpu_id():
    """Get current GPU ID from registry."""  # inserted
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000', 0, winreg.KEY_READ)
        gpu_id = winreg.QueryValueEx(key, 'DriverDesc')[0]
        winreg.CloseKey(key)
        return gpu_id if gpu_id else None
    except:
        return None

def get_current_disk_serial():
    """Get current disk serial number via vol or wmic."""  # inserted
    try:
        output = subprocess.check_output('vol C:', shell=True, stderr=subprocess.DEVNULL).decode().strip()
        serial = output.split('Volume Serial Number is ')[1].strip()
        return serial if serial else None
    except:
        try:
            output = subprocess.check_output('wmic diskdrive get SerialNumber', shell=True, stderr=subprocess.DEVNULL).decode().strip()
            for line in output.splitlines()[1:]:
                if line.strip():
                    return line.strip()
        except:
            pass
    return None

def clean_game_data():
    """Clean game tracking data for popular games."""  # inserted
    paths = [Path(os.getenv('APPDATA')) / 'FortniteGame', Path(os.getenv('APPDATA')) / 'EpicGamesLauncher', Path(os.getenv('LOCALAPPDATA')) / 'Riot Games', Path(os.getenv('APPDATA')) / 'Minecraft', Path(os.getenv('LOCALAPPDATA')) / 'Valorant']
    cleaned = False
    for path in paths:
        try:
            if path.exists():
                shutil.rmtree(path)
                print_gradient_text(f'[+] Cleaned: {path}')
                cleaned = True
        except:
            pass
    if not cleaned:
        print_gradient_text('[-] No game data found to clean.')
    return cleaned

def backup_hwids():
    """Backup all available HWIDs in memory."""  # inserted
    original_hwids['cpu'] = get_current_cpu_id()
    original_hwids['gpu'] = get_current_gpu_id()
    original_hwids['disk'] = get_current_disk_serial()
    print_gradient_text('[*] Backing up original HWIDs:')
    for key, value in original_hwids.items():
        if value:
            print_gradient_text(f'    - {key.upper()}: {value}')
        else:  # inserted
            print_gradient_text(f'    - {key.upper()}: Failed to retrieve, will skip spoofing.')
    if not any(original_hwids.values()):
        print_gradient_text('[-] Failed to backup any HWIDs. Aborting.')
        input(f'{Fore.RED}Press Enter to return to menu...{Style.RESET_ALL}')
    return False

def is_admin():
    """Check if the script is running with admin privileges."""  # inserted
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def spoof_hwids(simulate: bool=True):
    """Spoof CPU, GPU, and Disk HWIDs temporarily."""  # inserted
    global new_disk_serial  # inserted
    global spoofed  # inserted
    if not is_admin() and (not simulate):
        print_gradient_text('[-] Admin privileges required for live spoofing. Run as administrator.')
        print_gradient_text('[-] Use \'run_as_admin.bat\' in \'C:\\Users\\BX1\\Desktop\\nouveau projet\' to launch with admin rights.')
        input(f'{Fore.RED}Press Enter to return to menu...{Style.RESET_ALL}')
    return False

def restore_hwids():
    """Restore all original HWIDs from memory."""  # inserted
    global spoofed  # inserted
    if not spoofed:
        pass  # postinserted
    return None

def signal_handler(sig, frame):
    """Handle Ctrl+C to restore HWIDs and return to menu."""  # inserted
    if spoofed:
        print_gradient_text('[!] Ctrl+C detected. Restoring original HWIDs...')
        restore_hwids()
    os.system('cls')
    main()

def display_menu():
    """Display the interactive menu."""  # inserted
    os.system('cls')
    print_gradient_text('\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550')
    print_gradient_ascii(ASCII_ART)
    print_gradient_text('\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550')
    print_gradient_text('[!] PHANTOM VEIL SPOOFER ULTIMATE - ENGINEERED BY BX1')
    print_gradient_text('    \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557')
    print_gradient_text('    \u2551   Become a ghost. Spoof all HWIDs temporarily.       \u2551')
    print_gradient_text('    \u2551   What it spoofs:                                    \u2551')
    print_gradient_text('    \u2551   - CPU ID                                           \u2551')
    print_gradient_text('    \u2551   - GPU ID                                           \u2551')
    print_gradient_text('    \u2551   - Disk Serial                                      \u2551')
    print_gradient_text('    \u2551   - Cleaner: Game tracking data (Fortnite, etc.)     \u2551')
    print_gradient_text('    \u2551   - Safe: Auto-restores all IDs on exit.             \u2551')
    print_gradient_text('    \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d')
    print_gradient_text('[!] WARNING: Use in a VM for testing. Requires admin rights for live mode.')
    print_gradient_text('[!] Check HWIDs: Run commands in CMD (admin):')
    print_gradient_text('\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550')
    print_gradient_text('  [1] Launch Spoofing (Simulation Mode)')
    print_gradient_text('  [2] Launch Spoofing (Live Mode - Admin Required)')
    print_gradient_text('  [3] Clean Game Data')
    print_gradient_text('  [4] Exit')
    print_gradient_text('\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550')

def main():
    """Main function for Phantom Veil Spoofer."""
    signal.signal(signal.SIGINT, signal_handler)
    atexit.register(lambda: restore_hwids() if spoofed else None)
    
    while True:
        display_menu()
        choice = input(f'{Fore.RED}[?] Enter choice: {Style.RESET_ALL}').strip()
        
        if choice == '1':
            print_gradient_text('[*] Starting Simulation Mode...')
            set_seed()
            backup_hwids()
            spoof_hwids(simulate=True)
            input(f'{Fore.RED}Press Enter to continue...{Style.RESET_ALL}')
        elif choice == '2':
            print_gradient_text('[*] Starting Live Mode...')
            if not is_admin():
                print_gradient_text('[-] Admin privileges required for live spoofing. Run as administrator.')
            else:
                set_seed()
                backup_hwids()
                spoof_hwids(simulate=False)
            input(f'{Fore.RED}Press Enter to continue...{Style.RESET_ALL}')
        elif choice == '3':
            print_gradient_text('[*] Cleaning game data...')
            clean_game_data()
            input(f'{Fore.RED}Press Enter to continue...{Style.RESET_ALL}')
        elif choice == '4':
            print_gradient_text('[*] Exiting...')
            if spoofed:
                restore_hwids()
            break
        else:
            print_gradient_text('[-] Invalid choice. Try again.')

if __name__ == '__main__':
    main()
