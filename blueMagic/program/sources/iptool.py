# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'iptool.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import requests
import sys
import socket
import random
import subprocess
import platform
import ctypes
from colorama import init, Fore, Style
import time
import os
import hashlib
from time import sleep
from datetime import datetime, UTC

init()

ASCII_ART = '''
                          ..:-========-:..                    
                        .-===-:::::::-===-.                    
                      .-==-............:-==-.                  
                    ..-==:...............:==-..                
                    .-==::...............::-==.                
                    .==:::.............:::::-=-                
                    :==:::::.........:::::::-==                
                    :==:::::::::::::::::::::-==                
                    .==:::::::::::::::::::::-=-                
                    .-==:::::::::::::::::::-==.                
                    ..-==:::::::::::::::::-==..                
                      .-==-:::::::::::::-==-..                 
                        .-===-:::::::-====-.                   
                          .:-=========-====-.                  
                                       .==--=:                
                                        .=###*:               
                                         .+%###=.             
                                           -%###=.           
                                           .-####+.          
                                            .:#%##*.         
                                              .#%##*:        
                                               .+%%*:       
'''

def is_valid_ip(ip):
    """Validate IP address format."""
    try:
        socket.inet_aton(ip)
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False
        return True
    except:
        return False

def is_admin():
    """Check if the script is running with admin privileges (Windows)."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_ip_info(ip):
    """Get IP information from ipinfo.io."""
    if not is_valid_ip(ip):
        print(f'{Fore.GREEN}[-] Invalid IP address: {ip}{Style.RESET_ALL}')
        input(f'{Fore.GREEN}[ENTER] to exit...{Style.RESET_ALL}')
        sys.exit(0)
    try:
        url = f'https://ipinfo.io/{ip}/json'
        response = requests.get(url, timeout=5)
        if response.status_code == 404:
            print(f'{Fore.GREEN}[+] Status: invalid{Style.RESET_ALL}')
        else:
            print(f'{Fore.GREEN}[+] Status: valid{Style.RESET_ALL}')
        data = response.json()
        print(f'{Fore.GREEN}[+] IP Info:{Style.RESET_ALL}')
        for key, value in data.items():
            print(f'{Fore.GREEN}    {key}: {value}{Style.RESET_ALL}')
    except requests.RequestException as e:
        print(f'{Fore.GREEN}[-] Error fetching IP info: {e}{Style.RESET_ALL}')

def ip_pinger(ip):
    """Ping an IP address."""
    if not is_valid_ip(ip):
        print(f'{Fore.GREEN}[-] Invalid IP address: {ip}{Style.RESET_ALL}')
        input(f'{Fore.GREEN}[ENTER] to exit...{Style.RESET_ALL}')
        sys.exit(0)
    if not is_admin():
        print(f'{Fore.GREEN}[-] Admin privileges recommended for reliable ping. Run as administrator.{Style.RESET_ALL}')
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    try:
        result = subprocess.run(['ping', param, '1', ip], capture_output=True, text=True, timeout=10, encoding='cp1252')
        print(f'{Fore.GREEN}[*] Ping output: {result.stdout}{Style.RESET_ALL}')
        if result.stderr:
            print(f'{Fore.GREEN}[*] Ping error: {result.stderr}{Style.RESET_ALL}')
        if result.returncode == 0:
            print(f'{Fore.GREEN}[+] {ip} is reachable{Style.RESET_ALL}')
        else:
            print(f'{Fore.GREEN}[-] {ip} is unreachable{Style.RESET_ALL}')
    except subprocess.TimeoutExpired:
        print(f'{Fore.GREEN}[-] Ping timed out{Style.RESET_ALL}')
    except Exception as e:
        print(f'{Fore.GREEN}[-] Ping error: {e}{Style.RESET_ALL}')

def port_scanner(ip, ports=[80, 443, 22, 21, 25, 8080, 3389]):
    """Scan ports on an IP address."""
    if not is_valid_ip(ip):
        print(f'{Fore.GREEN}[-] Invalid IP address: {ip}{Style.RESET_ALL}')
        input(f'{Fore.GREEN}[ENTER] to exit...{Style.RESET_ALL}')
        sys.exit(0)
    print(f'{Fore.GREEN}[+] Scanning ports on {ip}...{Style.RESET_ALL}')
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f'{Fore.GREEN}[+] Port {port} is OPEN{Style.RESET_ALL}')
                open_ports.append(port)
            else:
                print(f'{Fore.RED}[-] Port {port} is CLOSED{Style.RESET_ALL}')
            sock.close()
        except socket.error as e:
            print(f'{Fore.GREEN}[-] Port {port} scan failed: {e}{Style.RESET_ALL}')
    if not open_ports:
        print(f'{Fore.GREEN}[-] No open ports found on {ip}{Style.RESET_ALL}')
    else:
        print(f'{Fore.GREEN}[+] Open ports: {open_ports}{Style.RESET_ALL}')

def ip_generator():
    """Generate a random IP address."""
    ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
    print(f'{Fore.GREEN}[+] Generated IP: {ip}{Style.RESET_ALL}')
    return ip

def main():
    """Main function for the tool."""
    print(f'{Fore.GREEN}{ASCII_ART}{Style.RESET_ALL}')
    print(f'{Fore.GREEN}[1] Get IP Info{Style.RESET_ALL}')
    print(f'{Fore.GREEN}[2] Ping IP{Style.RESET_ALL}')
    print(f'{Fore.GREEN}[3] Port Scan{Style.RESET_ALL}')
    print(f'{Fore.GREEN}[4] Generate Random IP{Style.RESET_ALL}')
    print(f'{Fore.GREEN}[5] Exit{Style.RESET_ALL}')
    
    choice = input(f'{Fore.GREEN}Choose an option: {Style.RESET_ALL}')
    
    if choice == '1':
        ip = input(f'{Fore.GREEN}Enter IP: {Style.RESET_ALL}')
        get_ip_info(ip)
    elif choice == '2':
        ip = input(f'{Fore.GREEN}Enter IP to ping: {Style.RESET_ALL}')
        ip_pinger(ip)
    elif choice == '3':
        ip = input(f'{Fore.GREEN}Enter IP to scan: {Style.RESET_ALL}')
        port_scanner(ip)
    elif choice == '4':
        ip_generator()
    elif choice == '5':
        print(f'{Fore.GREEN}[+] Exiting...{Style.RESET_ALL}')
        sys.exit(0)
    else:
        print(f'{Fore.GREEN}[-] Invalid choice{Style.RESET_ALL}')
    
    input(f'{Fore.GREEN}[ENTER] to exit...{Style.RESET_ALL}')

if __name__ == '__main__':
    main()
