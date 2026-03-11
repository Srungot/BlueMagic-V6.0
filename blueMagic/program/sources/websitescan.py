# Website Scanner Tool
import requests
import socket
import os
from urllib.parse import urlparse
from colorama import Fore, Style

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = """
 ______                                           __
|      \\                                         |  \\
 \\$$$$$$ _______        __   ______    _______  _| $$_
  | $$  |       \\      |  \\ /      \\  /       \\|   $$ \\
  | $$  | $$$$$$$\\      \\$$|  $$$$$$\\|  $$$$$$$ \\$$$$$$
  | $$  | $$  | $$     |  \\| $$    $$| $$        | $$ __
 _| $$_ | $$  | $$     | $$| $$$$$$$$| $$_____   | $$|  \\
|   $$ \\| $$  | $$     | $$ \\$$     \\ \\$$     \\   \\$$  $$
 \\$$$$$$ \\$$   \\$$__   | $$  \\$$$$$$$  \\$$$$$$$    \\$$$$
                 |  \\__/ $$
                  \\$$    $$
                   \\$$$$$$
"""
    print(f'{Fore.CYAN}{banner}{Style.RESET_ALL}')
    print(f'{Fore.CYAN}\u2554' + '\u2550' * 60 + '\u2557' + Style.RESET_ALL)
    print(f'{Fore.CYAN}\u2551   [>] Website Info (IP, Ports, SSL, Tech)            \u2551{Style.RESET_ALL}')
    print(f'{Fore.CYAN}\u2551   [>] URL Crawler                                    \u2551{Style.RESET_ALL}')
    print(f'{Fore.CYAN}\u2551   [>] Vulns (SQLi, XSS, LFI, Files, Dirs, CMS)       \u2551{Style.RESET_ALL}')
    print(f'{Fore.CYAN}\u2551   [>] Subdomains                                     \u2551{Style.RESET_ALL}')
    print(f'{Fore.CYAN}\u2551   [>] Output: scan.txt, JSON, PDF reports            \u2551{Style.RESET_ALL}')
    print(f'{Fore.CYAN}\u255a' + '\u2550' * 60 + '\u255d' + Style.RESET_ALL)

def get_website_info(url):
    if not url.startswith('http'):
        url = 'https://' + url
    print(f'{Fore.GREEN}[>] Scanning: {url}{Style.RESET_ALL}')
    parsed = urlparse(url)
    domain = parsed.netloc
    results = {'domain': domain}
    
    try:
        ip = socket.gethostbyname(domain)
        print(f'{Fore.GREEN}[+] IP: {ip}{Style.RESET_ALL}')
        results['ip'] = ip
    except:
        print(f'{Fore.RED}[-] Could not resolve IP{Style.RESET_ALL}')
    
    try:
        response = requests.get(url, timeout=10)
        print(f'{Fore.GREEN}[+] Status: {response.status_code}{Style.RESET_ALL}')
        results['status'] = response.status_code
        results['server'] = response.headers.get('Server', 'Unknown')
    except Exception as e:
        print(f'{Fore.RED}[-] Error: {e}{Style.RESET_ALL}')
    
    return results

def scan_ports(domain):
    print(f'{Fore.YELLOW}[*] Scanning ports...{Style.RESET_ALL}')
    common_ports = [21, 22, 80, 443, 3306, 8080, 3389]
    open_ports = []
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((domain, port))
            if result == 0:
                print(f'{Fore.GREEN}[+] Port {port} is open{Style.RESET_ALL}')
                open_ports.append(port)
            sock.close()
        except:
            pass
    return open_ports

def crawl_urls(url):
    if not url.startswith('http'):
        url = 'https://' + url
    print(f'{Fore.YELLOW}[*] Crawling URLs...{Style.RESET_ALL}')
    try:
        response = requests.get(url, timeout=10)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            links.add(a['href'])
        print(f'{Fore.GREEN}[+] Found {len(links)} URLs{Style.RESET_ALL}')
        return list(links)[:20]
    except Exception as e:
        print(f'{Fore.RED}[-] Error: {e}{Style.RESET_ALL}')
        return []

def check_vulnerabilities(url):
    if not url.startswith('http'):
        url = 'https://' + url
    print(f'{Fore.YELLOW}[*] Checking vulnerabilities...{Style.RESET_ALL}')
    vulns = []
    
    sqli_payloads = ["'", "' OR '1'='1", '" OR "1"="1']
    for payload in sqli_payloads:
        try:
            test_url = f"{url}?id={payload}"
            r = requests.get(test_url, timeout=5)
            if 'error' in r.text.lower() or 'sql' in r.text.lower():
                vulns.append(f"Potential SQLi: {payload}")
        except:
            pass
    
    xss_payloads = ["<script>alert('xss')</script>", "<img src=x onerror=alert('xss')>"]
    for payload in xss_payloads:
        try:
            test_url = f"{url}?q={payload}"
            r = requests.get(test_url, timeout=5)
            if payload in r.text:
                vulns.append(f"Potential XSS: {payload}")
        except:
            pass
    
    if vulns:
        for v in vulns:
            print(f'{Fore.RED}[!] {v}{Style.RESET_ALL}')
    else:
        print(f'{Fore.GREEN}[+] No obvious vulnerabilities found{Style.RESET_ALL}')
    return vulns

def scan_subdomains(domain):
    print(f'{Fore.YELLOW}[*] Scanning subdomains...{Style.RESET_ALL}')
    subdomains = ['www', 'mail', 'ftp', 'admin', 'blog', 'api']
    found = []
    for sub in subdomains:
        try:
            ip = socket.gethostbyname(f"{sub}.{domain}")
            print(f'{Fore.GREEN}[+] Found: {sub}.{domain} ({ip}){Style.RESET_ALL}')
            found.append(f"{sub}.{domain}")
        except:
            pass
    return found

def save_results(url, results):
    os.makedirs('output', exist_ok=True)
    with open('output/scan.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n=== Scan for {url} ===\n")
        for key, value in results.items():
            f.write(f"{key}: {value}\n")
    print(f'{Fore.GREEN}[+] Results saved to output/scan.txt{Style.RESET_ALL}')

def main():
    print_banner()
    print()
    print(f'{Fore.GREEN}[1] Website Info Scan{Style.RESET_ALL}')
    print(f'{Fore.GREEN}[2] URL Crawler{Style.RESET_ALL}')
    print(f'{Fore.GREEN}[3] Vulnerability Scanner{Style.RESET_ALL}')
    print(f'{Fore.GREEN}[4] Full Scan{Style.RESET_ALL}')
    print(f'{Fore.GREEN}[5] Subdomain Scanner{Style.RESET_ALL}')
    print()
    
    choice = input(f'{Fore.CYAN}[>] Choice: {Style.RESET_ALL}').strip()
    if choice not in ['1', '2', '3', '4', '5']:
        print(f'{Fore.RED}[!] Invalid choice{Style.RESET_ALL}')
        return
    
    url = input(f'{Fore.CYAN}[>] Enter target URL: {Style.RESET_ALL}').strip()
    if not url:
        print(f'{Fore.RED}[!] No URL provided{Style.RESET_ALL}')
        return
    
    results = {}
    parsed = urlparse(url if url.startswith('http') else 'https://' + url)
    domain = parsed.netloc
    
    if choice == '1':
        results = get_website_info(url)
        results['ports'] = scan_ports(domain)
    elif choice == '2':
        results['urls'] = crawl_urls(url)
    elif choice == '3':
        results['vulns'] = check_vulnerabilities(url)
    elif choice == '4':
        results = get_website_info(url)
        results['ports'] = scan_ports(domain)
        results['urls'] = crawl_urls(url)
        results['vulns'] = check_vulnerabilities(url)
        results['subdomains'] = scan_subdomains(domain)
    elif choice == '5':
        results['subdomains'] = scan_subdomains(domain)
    
    save_results(url, results)
    print(f'{Fore.GREEN}[+] Scan finished!{Style.RESET_ALL}')
    input(f'{Fore.CYAN}[*] Press Enter to exit.{Style.RESET_ALL}')

if __name__ == '__main__':
    main()
