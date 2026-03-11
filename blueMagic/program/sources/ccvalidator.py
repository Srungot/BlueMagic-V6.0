# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'ccvalidator.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import re
import requests
from colorama import Fore
import sys
import os

USER_AGENT_FILE = 'input/user-agents.txt'
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'

def load_user_agents():
    if not os.path.exists(USER_AGENT_FILE):
        print(Fore.YELLOW + f'[!] Fichier {USER_AGENT_FILE} manquant. Utilisation user-agent par défaut.')
        return [DEFAULT_USER_AGENT]
    with open(USER_AGENT_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def luhn_check(card_number):
    card_number = [int(digit) for digit in str(card_number)]
    checksum = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0

def get_card_brand(card_number):
    brands = {
        r'^4[0-9]{12}(?:[0-9]{3})?$': 'Visa',
        r'^5[1-5][0-9]{14}$': 'MasterCard',
        r'^3[47][0-9]{13}$': 'American Express',
        r'^6(?:011|5[0-9]{2})[0-9]{12}$': 'Discover',
        r'^3(?:0[0-5]|[68][0-9])[0-9]{11}$': 'Diners Club',
        r'^(?:2131|1800|35\d{3})\d{11}$': 'JCB'
    }
    for pattern, brand in brands.items():
        if re.match(pattern, card_number):
            return brand
    return 'Unknown'

def get_bin_info(card_number):
    bin_number = card_number[:6]
    url = f'https://lookup.binlist.net/{bin_number}'
    try:
        response = requests.get(url, headers={'User-Agent': DEFAULT_USER_AGENT}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                'Bank': data.get('bank', {}).get('name', 'Unknown'),
                'Country': data.get('country', {}).get('name', 'Unknown'),
                'Type': data.get('type', 'Unknown'),
                'Brand': data.get('scheme', 'Unknown').capitalize()
            }
    except Exception:
        pass
    return {'Error': 'cc invalid'}

def validate_card(card_number):
    card_number = card_number.replace(' ', '').replace('-', '')
    if not card_number.isdigit():
        return False, 'Invalid format'
    if not luhn_check(card_number):
        return False, 'Luhn check failed'
    brand = get_card_brand(card_number)
    bin_info = get_bin_info(card_number)
    return True, {'Brand': brand, **bin_info}

def main():
    print(Fore.CYAN + '=== CC Validator ===' + Fore.RESET)
    while True:
        card = input(Fore.YELLOW + 'Enter card number (or q to quit): ' + Fore.RESET).strip()
        if card.lower() == 'q':
            break
        valid, info = validate_card(card)
        if valid:
            print(Fore.GREEN + f'[+] Valid card: {info}' + Fore.RESET)
        else:
            print(Fore.RED + f'[-] Invalid card: {info}' + Fore.RESET)

if __name__ == '__main__':
    main()
