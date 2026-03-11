# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'doxtool.py'
# Bytecode version: 3.13.0rc3 (3571)
import discord
from discord.ext import commands
import requests
import re
import asyncio
from colorama import Fore, Style

BLUE = '\033[94m'
RED = '\033[91m'
RESET = '\033[0m'

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def clean_username(username):
    return re.sub(r'#\d+$', '', username)

async def discord_dox(target_id):
    print(f'{Fore.LIGHTCYAN_EX}[+] Fetching Discord info...{RESET}')
    results = {'discord_info': {}}
    try:
        user = await bot.fetch_user(int(target_id))
        full_username = f'{user.name}#{user.discriminator}' if user.discriminator != '0' else user.name
        results['discord_info'] = {
            'username': full_username,
            'clean_username': clean_username(full_username),
            'id': str(user.id),
            'created_at': str(user.created_at),
            'avatar': str(user.avatar.url) if user.avatar else 'No avatar',
            'servers': [guild.name for guild in user.mutual_guilds]
        }
    except discord.errors.HTTPException as e:
        results['discord_info'] = {'error': f'Error: {str(e)}. Bot must share a server with user.'}
    except Exception as e:
        results['discord_info'] = {'error': f'General error: {str(e)}'}
    return results

def external_dox(username):
    print(f'{Fore.LIGHTCYAN_EX}[+] Scanning external platforms...{RESET}')
    clean_name = clean_username(username)
    results = {
        'youtube': ['No profile found'],
        'tiktok': ['No profile found'],
        'snapchat': ['No profile found'],
        'instagram': ['No profile found'],
        'github': ['No profile found']
    }
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Check GitHub
    print(f'{Fore.LIGHTCYAN_EX}[+] Checking GitHub...{RESET}')
    github_url = f'https://github.com/{clean_name}'
    try:
        r = requests.get(github_url, headers=headers, timeout=10)
        if r.status_code == 200:
            results['github'] = [github_url]
    except:
        pass
    
    # Check Instagram
    print(f'{Fore.LIGHTCYAN_EX}[+] Checking Instagram...{RESET}')
    insta_url = f'https://www.instagram.com/{clean_name}/'
    try:
        r = requests.get(insta_url, headers=headers, timeout=10)
        if r.status_code == 200:
            results['instagram'] = [insta_url]
    except:
        pass
    
    # Check TikTok
    print(f'{Fore.LIGHTCYAN_EX}[+] Checking TikTok...{RESET}')
    tiktok_url = f'https://www.tiktok.com/@{clean_name}'
    try:
        r = requests.get(tiktok_url, headers=headers, timeout=10)
        if r.status_code == 200:
            results['tiktok'] = [tiktok_url]
    except:
        pass
    
    return results

def print_results(discord_data, external_data):
    print(f'\n{Fore.LIGHTCYAN_EX}=== Discord Results ==={RESET}')
    discord_info = discord_data.get('discord_info', {})
    
    if 'error' not in discord_info:
        print(f'{Fore.LIGHTCYAN_EX}Username: {discord_info.get("username", "N/A")}{RESET}')
        print(f'{Fore.LIGHTCYAN_EX}Cleaned Username: {discord_info.get("clean_username", "N/A")}{RESET}')
        print(f'{Fore.LIGHTCYAN_EX}ID: {discord_info.get("id", "N/A")}{RESET}')
        print(f'{Fore.LIGHTCYAN_EX}Avatar: {discord_info.get("avatar", "N/A")}{RESET}')
        print(f'{Fore.LIGHTCYAN_EX}Creation Date: {discord_info.get("created_at", "N/A")}{RESET}')
        servers = ', '.join(discord_info.get('servers', [])) or 'None'
        print(f'{Fore.LIGHTCYAN_EX}Common Servers: {servers}{RESET}')
    else:
        print(f'{Fore.LIGHTCYAN_EX}Error: {discord_info["error"]}{RESET}')
    
    print(f'\n{Fore.LIGHTCYAN_EX}=== External Results ==={RESET}')
    for platform, links in external_data.items():
        platform_name = platform.capitalize()
        print(f'{Fore.LIGHTCYAN_EX}{platform_name}:{RESET}')
        for link in links:
            print(f'{Fore.LIGHTCYAN_EX}  - {link}{RESET}')

@bot.event
async def on_ready():
    print(f'{Fore.LIGHTCYAN_EX}✅ Bot connected: {bot.user.name}{RESET}')
    
    while True:
        target_id = input(f'{Fore.LIGHTCYAN_EX}[+] Enter Discord ID (or "quit"): {RESET}').strip()
        
        if target_id.lower() == 'quit':
            print(f'{Fore.LIGHTCYAN_EX}[-] Exiting...{RESET}')
            await bot.close()
            break
        
        if not target_id.isdigit() or len(target_id) not in [17, 18, 19, 20]:
            print(f'{Fore.LIGHTCYAN_EX}[-] Invalid ID: Must be 17-20 digits.{RESET}')
            continue
        
        discord_data = await discord_dox(target_id)
        clean_name = discord_data.get('discord_info', {}).get('clean_username', '')
        
        if clean_name:
            external_data = external_dox(clean_name)
        else:
            external_data = {}
        
        print_results(discord_data, external_data)

async def main():
    print(f'{Fore.LIGHTCYAN_EX}')
    print('''
    ╔═══════════════════════════════════════╗
    ║           DOX TOOL v1.0                ║
    ╚═══════════════════════════════════════╝
    ''')
    print(f'{RESET}')
    
    token = input(f'{Fore.LIGHTCYAN_EX}[+] Enter Discord bot token: {RESET}').strip()
    
    if not token:
        print(f'{Fore.LIGHTCYAN_EX}[-] No token provided.{RESET}')
        return
    
    try:
        await bot.start(token)
    except discord.errors.LoginFailure:
        print(f'{Fore.LIGHTCYAN_EX}[-] Invalid token.{RESET}')
    except Exception as e:
        print(f'{Fore.LIGHTCYAN_EX}[-] Error: {e}{RESET}')

if __name__ == '__main__':
    asyncio.run(main())
