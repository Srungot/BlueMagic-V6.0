# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'Token Tool.py'
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import os
import requests
import string
import random
import threading
import time
import json
from datetime import datetime, timezone
from colorama import Fore

RESET = '\x1b[0m'
WHITE = '\x1b[97m'
RED = '\x1b[91m'
GREEN = '\x1b[92m'
YELLOW = '\x1b[93m'
BLUE = '\x1b[94m'

TOKEN_FILE = 'input/token.txt'

def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []

def print_boxed(info_dict):
    line = '\u2500' * 60
    print(f'{WHITE}{line}{RESET}')
    for key, value in info_dict.items():
        print(f'{YELLOW}{key:20}:{WHITE} {value}{RESET}')
    print(f'{WHITE}{line}{RESET}')

def get_token_info(token):
    try:
        api = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token}).json()
        response = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
        status = 'Valid' if response.status_code == 200 else 'Invalid'
        username = api.get('username', 'None') + '#' + api.get('discriminator', 'None')
        user_id = api.get('id', 'None')
        email = api.get('email', 'None')
        phone = api.get('phone', 'None')
        mfa = api.get('mfa_enabled', 'None')
        country = api.get('locale', 'None')
        avatar = api.get('avatar', 'None')
        nitro = 'None'
        try:
            created_at = datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000, timezone.utc)
        except:
            created_at = 'None'
        return {'Status': status, 'Token': token, 'Username': username, 'Id': user_id, 'Created': created_at, 'Country': country, 'Email': email, 'Phone': phone, 'MFA': mfa, 'Nitro': nitro, 'Avatar': avatar}
    except Exception as e:
        return {'Status': 'Invalid', 'Token': token, 'Error': str(e)}

def token_login():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}\u274c No tokens found in input/token.txt{RESET}')
        input('Press Enter to return to menu...')
        return
    print(f'{YELLOW}Testing all tokens from input/token.txt...{RESET}')
    for token in tokens:
        info = get_token_info(token)
        print_boxed(info)
    input('Press Enter to return to menu...')

def generate_single_token():
    first = ''.join(random.choice(string.ascii_letters + string.digits + '-_') for _ in range(random.choice([24, 26])))
    second = ''.join(random.choice(string.ascii_letters + string.digits + '-_') for _ in range(6))
    third = ''.join(random.choice(string.ascii_letters + string.digits + '-_') for _ in range(38))
    return f'{first}.{second}.{third}'

def token_check(token):
    try:
        user = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token}).json()
        user['username']
        print(f'{GREEN}\u2705 Valid Token: {token}{RESET}')
        return True
    except:
        print(f'{RED}\u274c Invalid Token: {token}{RESET}')
        return False

def token_generator():
    print(f'{YELLOW}Generates random Discord tokens and validates them.{RESET}')
    try:
        threads_number = int(input('Number of threads -> '))
    except:
        print(f'{RED}\u274c Invalid input{RESET}')
        input('Press Enter to return to menu...')
        return
    
    def worker():
        token = generate_single_token()
        token_check(token)
    
    print(f'{YELLOW}Press CTRL+C to stop token generation.{RESET}')
    try:
        while True:
            threads = []
            for _ in range(threads_number):
                t = threading.Thread(target=worker)
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
    except KeyboardInterrupt:
        print(f'{YELLOW}Stopping token generation.{RESET}')
    input('Press Enter to return to menu...')

def token_nuker():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}\u274c No tokens found{RESET}')
        input('Press Enter to return...')
        return
    token = tokens[0]
    custom_status = input('Custom Status -> ').strip()
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    try:
        while True:
            requests.patch('https://discord.com/api/v9/users/@me/settings', headers=headers, json={'custom_status': {'text': custom_status}})
            print(f'{GREEN}\u2705 Status set: {custom_status}{RESET}')
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f'{YELLOW}\u26a0\ufe0f Nuker stopped{RESET}')
    input('Press Enter to return to menu...')

def token_joiner():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}\u274c No tokens found{RESET}')
        input('Press Enter to return...')
        return
    token = tokens[0]
    invite = input('Invite link -> ').strip()
    invite_code = invite.split('/')[-1]
    try:
        r = requests.post(f'https://discord.com/api/v9/invites/{invite_code}', headers={'Authorization': token})
        if r.status_code == 200:
            print(f'{GREEN}\u2705 Joined server{RESET}')
        else:
            print(f'{RED}\u274c Failed to join{RESET}')
    except:
        print(f'{RED}\u274c Error{RESET}')
    input('Press Enter to return to menu...')

def token_leaver():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}\u274c No tokens found{RESET}')
        input('Press Enter to return...')
        return
    token = tokens[0]
    try:
        guilds = requests.get('https://discord.com/api/v8/users/@me/guilds', headers={'Authorization': token}).json()
        for guild in guilds:
            guild_id = guild['id']
            r = requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{guild_id}', headers={'Authorization': token})
            if r.status_code in [200, 204]:
                print(f'{GREEN}\u2705 Left: {guild.get("name", guild_id)}{RESET}')
    except Exception as e:
        print(f'{RED}\u274c Error: {e}{RESET}')
    input('Press Enter to return to menu...')

def token_spammer():
    tokens = load_tokens()
    if not tokens:
        print(f'{RED}\u274c No tokens found{RESET}')
        input('Press Enter to return...')
        return
    token = tokens[0]
    target_id = input('Target Channel ID -> ').strip()
    message = input('Message -> ').strip()
    try:
        count = int(input('Number of messages -> '))
    except:
        print(f'{RED}\u274c Invalid input{RESET}')
        input('Press Enter to return...')
        return
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    for i in range(count):
        try:
            r = requests.post(f'https://discord.com/api/v9/channels/{target_id}/messages', headers=headers, json={'content': message})
            if r.status_code in [200, 201]:
                print(f'{GREEN}\u2705 Message {i+1} sent{RESET}')
            else:
                print(f'{RED}\u274c Failed message {i+1}{RESET}')
        except Exception as e:
            print(f'{RED}\u274c Error: {e}{RESET}')
    input('Press Enter to return to menu...')

def token_info():
    token = input('Token -> ').strip()
    info = get_token_info(token)
    print_boxed(info)
    input('Press Enter to return to menu...')

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'{Fore.LIGHTCYAN_EX}=== Discord Token-Tool Panel ===')
        print('1  Token Login')
        print('2  Token Info')
        print('3  Token Generator')
        print('4  Token Nuker')
        print('5  Token Joiner')
        print('6  Token Leaver')
        print('7  Token Spammer')
        print('8  Exit')
        print()
        choice = input('Your choice -> ').strip()
        if choice == '1':
            token_login()
        elif choice == '2':
            token_info()
        elif choice == '3':
            token_generator()
        elif choice == '4':
            token_nuker()
        elif choice == '5':
            token_joiner()
        elif choice == '6':
            token_leaver()
        elif choice == '7':
            token_spammer()
        elif choice == '8':
            print('Exiting...')
            break
        else:
            print(f'{RED}Invalid choice{RESET}')

if __name__ == '__main__':
    main_menu()
