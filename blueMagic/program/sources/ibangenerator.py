# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'ibangenerator.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import os
import random
from colorama import Fore, Style, init
import sys
import hashlib
from time import sleep
from datetime import datetime, UTC
init(autoreset=True)

iban_formats = {
    'FR': {'length': 27, 'bban': 'BBBBBGSSSCCCCCCCCCCCCCCC', 'name': 'France'},
    'DE': {'length': 22, 'bban': 'BBBBBBBBCCCCCCCCCC', 'name': 'Germany'},
    'ES': {'length': 24, 'bban': 'BBBBGSSSCCCCCCCCCCCC', 'name': 'Spain'},
    'IT': {'length': 27, 'bban': 'KBBBBBBSSSSSCCCCCCCCCCCC', 'name': 'Italy'},
    'GB': {'length': 22, 'bban': 'BBBBSSSSSSCCCCCCCCCC', 'name': 'United Kingdom'},
    'BE': {'length': 16, 'bban': 'BBBCCCCCCCCCC', 'name': 'Belgium'},
    'NL': {'length': 18, 'bban': 'BBBBCCCCCCCCCC', 'name': 'Netherlands'},
    'CH': {'length': 21, 'bban': 'BBBBBCCCCCCCCCCC', 'name': 'Switzerland'},
    'PT': {'length': 25, 'bban': 'BBBBSSSSCCCCCCCCCCCCCA', 'name': 'Portugal'},
    'AT': {'length': 20, 'bban': 'BBBBBCCCCCCCCCC', 'name': 'Austria'}
}

ascii_banner = Fore.RED + '''
 ______  _______    ______   __    __        ________  _______    ______   __    __  _______  
|      \|       \  /      \ |  \  |  \      |        \|       \  /      \ |  \  |  \|       \ 
 \$$$$$$| $$$$$$$\|  $$$$$$\| $$\ | $$      | $$$$$$$$| $$$$$$$\|  $$$$$$\| $$  | $$| $$$$$$$\
  | $$  | $$__/ $$| $$__| $$| $$$\| $$      | $$__    | $$__| $$| $$__| $$| $$  | $$| $$  | $$
  | $$  | $$    $$| $$    $$| $$$$\ $$      | $$  \   | $$    $$| $$    $$| $$  | $$| $$  | $$
  | $$  | $$$$$$$\| $$$$$$$$| $$\$$ $$      | $$$$$   | $$$$$$$\| $$$$$$$$| $$  | $$| $$  | $$
 _| $$_ | $$__/ $$| $$  | $$| $$ \$$$$      | $$      | $$  | $$| $$  | $$| $$__/ $$| $$__/ $$
|   $$ \| $$    $$| $$  | $$| $$  \$$$      | $$      | $$  | $$| $$  | $$ \$$    $$| $$    $$
 \$$$$$$ \$$$$$$$  \$$   \$$ \$$   \$$       \$$       \$$   \$$ \$$   \$$  \$$$$$$  \$$$$$$$ 

FRAUD IBAN GENERATOR by BX1 v1.1

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
''' + Style.RESET_ALL

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_bban(country_code):
    format_str = iban_formats[country_code]['bban']
    result = ''
    for char in format_str:
        if char in 'BGSKC':
            result += str(random.randint(0, 9))
        else:
            result += char
    return result

def calculate_check_digits(country_code, bban):
    temp = bban + country_code + '00'
    temp = temp.replace('A', '10').replace('B', '11').replace('C', '12').replace('D', '13')
    temp = temp.replace('E', '14').replace('F', '15').replace('G', '16').replace('H', '17')
    temp = temp.replace('I', '18').replace('J', '19').replace('K', '20').replace('L', '21')
    temp = temp.replace('M', '22').replace('N', '23').replace('O', '24').replace('P', '25')
    temp = temp.replace('Q', '26').replace('R', '27').replace('S', '28').replace('T', '29')
    temp = temp.replace('U', '30').replace('V', '31').replace('W', '32').replace('X', '33')
    temp = temp.replace('Y', '34').replace('Z', '35')
    num = int(temp)
    check = 98 - (num % 97)
    return str(check).zfill(2)

def generate_iban(country_code):
    bban = generate_bban(country_code)
    check_digits = calculate_check_digits(country_code, bban)
    return f'{country_code}{check_digits}{bban}'

def generate_multiple_ibans(country_code, count=1):
    return [generate_iban(country_code) for _ in range(count)]

def menu():
    clear()
    print(ascii_banner)
    items = [f"[{i+1}] {iban_formats[code]['name']} ({code})" for i, code in enumerate(iban_formats.keys())]
    items.append("[0] Exit")
    col_count = 2
    rows = -(-len(items) // col_count)
    for r in range(rows):
        line_parts = []
        for c in range(col_count):
            i = r + c * rows
            if i < len(items):
                line_parts.append(f"{items[i]:<40}")
        print(Fore.RED + ''.join(line_parts) + Style.RESET_ALL)
    choice = input(Fore.RED + '\n\n\n→ Country : ' + Style.RESET_ALL).strip('[]')
    if choice == '0':
        print(Fore.RED + '\nClosing generator...' + Style.RESET_ALL)
        sys.exit()
    try:
        country_code = list(iban_formats.keys())[int(choice) - 1]
    except:
        print(Fore.RED + 'Invalid input.' + Style.RESET_ALL)
        return
    count = input(Fore.RED + 'How many IBANs to generate? (default=1): ' + Style.RESET_ALL) or '1'
    count = int(count)
    print(ascii_banner)
    print(Fore.RED + f"--- IBANs generated for {iban_formats[country_code]['name']} ---\n" + Style.RESET_ALL)
    for iban in generate_multiple_ibans(country_code, count):
        print(Fore.RED + iban + Style.RESET_ALL)
    input(Fore.RED + '\nPress Enter to continue...' + Style.RESET_ALL)

def main():
    while True:
        menu()

if __name__ == '__main__':
    main()
