# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: phishing.py
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
from concurrent.futures import ThreadPoolExecutor
import re
from colorama import Fore
import sys
import time
import platform
import hashlib
from time import sleep
from datetime import datetime, UTC

def clear_screen():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

def getchecksum():
    md5_hash = hashlib.md5()
    with open(sys.argv[0], 'rb') as file:
        md5_hash.update(file.read())
    return md5_hash.hexdigest()

# KeyAuth initialization (optional - remove if not needed)
try:
    from keyauth import api
    keyauthapp = api(name='exo', ownerid='rPFqetg2la', version='1.0', hash_to_check=getchecksum())
    try:
        with open(os.path.join('input', 'key.txt'), 'r', encoding='utf-8') as f:
            license_key = f.read().strip()
        keyauthapp.license(license_key)
        clear_screen()
    except Exception as e:
        print(f"KeyAuth error: {e}")
except ImportError:
    print("KeyAuth not installed, skipping license check...")

with open('input/user-agents.txt', 'r', encoding='utf-8') as f:
    user_agents = f.read().splitlines()

if user_agents:
    user_agent = random.choice(user_agents)
else:
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

headers = {'User-Agent': user_agent}

print(Fore.RED, '''
                                                       
                                    ............=@@@@@@*@@@+@@@@@+............      
                                    ............:@@@@@%@@@@@@@@=@@@@@=............    
                                ............-@@@@+@@@#=**-@@@@@@@@@@............    
                                ...........*@@@*@@@@%#++###@@@@@#@@@@=...........   
                                ..........=@@@:@@@@@##@@#%@@@@@@@@%@@@@..........   
                                .........#@@@@@@@@@@@@@@@@%@@@@@@@@@=@@@@:.......   
                                ........=@@@%@@@@@@@@@%=..:..-+%@@@@@@@*@@@*........ 
                                .......%@@%@@@@@*--:-%@@@@@@@@@*:==+*@@@@=@@+....... 
                                ......+@@@@@@*:.  .*@@@@*:+@@@@@@=.   .=@@@@@:...... 
                                ......@@@@@+.    .=@@#:=@@@#..=@@@:    .:#@*@-... .. 
                                ......@*@%.      .*@@:.=@+@@: .:@@:      .@+@-....   
                                ......@+@+.      .=@@@@@@-@%: .=@@:    .:*%-#:...... 
                                ......#%+@-.     .:+@@@@+%@*.=@@@#.   .-*#.%=....    
                                .....-@**#-..     ..:.-@@#=@@@@#:  ..-#+-%+....     
                                    .....=%++@*..       .*@@+@@@#-.  .:*@@@%-.....    
                                    ...-@@@@@@*:..     :#@#@@+.    .:*@@@@@@@+...    
                                    -@@@@@@+*@@*:..   .+@@-#@@-.  .:*@@@:+@@@@@@=    
                                :@@@@@#%@@@++#+-.. .=@@@%@@@@: .:+#@@#-@@@#@@@@@-   
                                -@@@@+@@@@#--=-==:. .*@@:..-@@- .-#-%@@%@@@@@@%@@@:  
                                =@@@%@@@@@#*=-=-.+-...+@@@%%@@@:..:@=@%@@#=%@@@@@@@#  
                                @@@@@@@@@#-++-=-=*+::.:*@@@@@@+.-=-@-@-+@@#=@%%@@@@@+ 
                                @@@@@@@@@-.=+---+=#:.:..:+#*=..:+==@:@=:=@@*@-+@@@@@@ 
''', Fore.RESET)

print(f'[+] Selected User-Agent : {user_agent}')
url = input('[+] URL : ').strip()

if 'https://' not in url and 'http://' not in url:
    url = 'https://' + url

try:
    session = requests.Session()
    session.headers.update(headers)
    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    css_links = soup.find_all('link', rel='stylesheet')
    script_links = soup.find_all('script', src=True)
    css_urls = [urljoin(url, link['href']) for link in css_links]
    js_urls = [urljoin(url, script['src']) for script in script_links]

    def fetch_text(u):
        try:
            return session.get(u, timeout=10).text
        except:
            return ''

    with ThreadPoolExecutor() as pool:
        css_contents = list(pool.map(fetch_text, css_urls))
        js_contents = list(pool.map(fetch_text, js_urls))

    if css_contents:
        style_tag = soup.new_tag('style')
        style_tag.string = '\n'.join(css_contents)
        soup.head.append(style_tag)
        for link in css_links:
            link.decompose()

    if js_contents:
        script_tag = soup.new_tag('script')
        script_tag.string = '\n'.join(js_contents)
        soup.body.append(script_tag)
        for script in script_links:
            script.decompose()

    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('www.', '')
    save_path = 'output'
    os.makedirs(save_path, exist_ok=True)
    file_name = re.sub('[\\\\/:*?"<>|]', '-', domain if domain else 'page_complet') + '.html'
    file_html = os.path.join(save_path, file_name)
    
    with open(file_html, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    
    print(f'[+] successful phishing attack : {file_html}')
    input()

except Exception as e:
    print(f'[+] phishing attack fail: {e}')
    input()
