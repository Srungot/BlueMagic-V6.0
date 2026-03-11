# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'bruteforce_zip.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import zipfile
import os
import time
import sys
from tqdm import tqdm
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(Fore.CYAN + '''
    ╔══════════════════════════════╗
    ║     ZIP BRUTEFORCE TOOL       ║
    ╚══════════════════════════════╝
    ''' + Style.RESET_ALL)

def try_password(zip_path, password):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(pwd=password.encode())
            return True
    except:
        return False

def bruteforce(zip_path, wordlist_path):
    if not os.path.exists(zip_path):
        print(Fore.RED + f'[!] ZIP file not found: {zip_path}' + Style.RESET_ALL)
        return None
    
    if not os.path.exists(wordlist_path):
        print(Fore.RED + f'[!] Wordlist not found: {wordlist_path}' + Style.RESET_ALL)
        return None
    
    print(Fore.GREEN + f'[*] Starting bruteforce on {zip_path}' + Style.RESET_ALL)
    
    with open(wordlist_path, 'r', errors='ignore') as f:
        passwords = [line.strip() for line in f if line.strip()]
    
    for password in tqdm(passwords, desc='Testing passwords'):
        if try_password(zip_path, password):
            print(Fore.GREEN + f'\n[+] Password found: {password}' + Style.RESET_ALL)
            return password
    
    print(Fore.RED + '\n[!] Password not found in wordlist' + Style.RESET_ALL)
    return None

def main():
    clear()
    banner()
    zip_path = input(Fore.YELLOW + '[?] Enter ZIP file path: ' + Style.RESET_ALL).strip()
    wordlist_path = input(Fore.YELLOW + '[?] Enter wordlist path: ' + Style.RESET_ALL).strip()
    bruteforce(zip_path, wordlist_path)
    input('\nPress Enter to exit...')

if __name__ == '__main__':
    main()
