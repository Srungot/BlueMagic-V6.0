# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'email_tool.py'
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
import time
import random
import re
import dns.resolver
from colorama import Fore, Style

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(Fore.CYAN + '''
    ╔═══════════════════════════════════════╗
    ║          EMAIL TOOL v1.0              ║
    ╚═══════════════════════════════════════╝
    ''' + Style.RESET_ALL)

def get_mx_records(domain):
    """Get MX records for a domain"""
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return [(r.exchange.to_text(), r.preference) for r in records]
    except Exception as e:
        print(f'{Fore.RED}[!] Error getting MX records: {e}{Style.RESET_ALL}')
        return []

def verify_email(email):
    """Verify if email exists using SMTP"""
    domain = email.split('@')[1]
    mx_records = get_mx_records(domain)
    
    if not mx_records:
        return False, "No MX records found"
    
    mx_host = mx_records[0][0]
    
    try:
        server = smtplib.SMTP(timeout=10)
        server.connect(mx_host, 25)
        server.ehlo_or_helo_if_needed()
        server.mail('test@example.com')
        code, message = server.rcpt(email)
        server.quit()
        
        if code == 250:
            return True, "Valid"
        else:
            return False, f"Invalid (code: {code})"
    except Exception as e:
        return False, str(e)

def send_email(sender, password, recipient, subject, body, smtp_server='smtp.gmail.com', port=587):
    """Send an email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        
        print(f'{Fore.GREEN}[+] Email sent to {recipient}{Style.RESET_ALL}')
        return True
    except Exception as e:
        print(f'{Fore.RED}[!] Error sending email: {e}{Style.RESET_ALL}')
        return False

def mass_email(sender, password, recipients_file, subject, body, smtp_server='smtp.gmail.com', port=587):
    """Send mass emails from a file"""
    if not os.path.exists(recipients_file):
        print(f'{Fore.RED}[!] File not found: {recipients_file}{Style.RESET_ALL}')
        return
    
    with open(recipients_file, 'r') as f:
        recipients = [line.strip() for line in f if line.strip()]
    
    print(f'{Fore.CYAN}[*] Sending to {len(recipients)} recipients...{Style.RESET_ALL}')
    
    success = 0
    for recipient in recipients:
        if send_email(sender, password, recipient, subject, body, smtp_server, port):
            success += 1
            time.sleep(random.uniform(1, 3))  # Random delay to avoid detection
    
    print(f'{Fore.GREEN}[+] Sent {success}/{len(recipients)} emails{Style.RESET_ALL}')

def generate_temp_email():
    """Generate a temporary email using 1secmail API"""
    try:
        domains = requests.get('https://www.1secmail.com/api/v1/', params={'action': 'getDomainList'}).json()
        domain = random.choice(domains)
        username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
        email = f'{username}@{domain}'
        print(f'{Fore.GREEN}[+] Temp email: {email}{Style.RESET_ALL}')
        return email, username, domain
    except Exception as e:
        print(f'{Fore.RED}[!] Error: {e}{Style.RESET_ALL}')
        return None, None, None

def check_inbox(username, domain):
    """Check inbox for temp email"""
    try:
        response = requests.get(f'https://www.1secmail.com/api/v1/', params={
            'action': 'getMessages',
            'login': username,
            'domain': domain
        }).json()
        
        if not response:
            print(f'{Fore.YELLOW}[*] No messages{Style.RESET_ALL}')
            return []
        
        for msg in response:
            print(f'{Fore.CYAN}[{msg["date"]}] From: {msg["from"]} - Subject: {msg["subject"]}{Style.RESET_ALL}')
        return response
    except Exception as e:
        print(f'{Fore.RED}[!] Error: {e}{Style.RESET_ALL}')
        return []

def main():
    clear()
    banner()
    
    while True:
        print(f'\n{Fore.CYAN}Options:{Style.RESET_ALL}')
        print('1. Verify Email')
        print('2. Send Email')
        print('3. Mass Email')
        print('4. Generate Temp Email')
        print('5. Check Temp Inbox')
        print('0. Exit')
        
        choice = input(f'{Fore.CYAN}[?] Choice: {Style.RESET_ALL}').strip()
        
        if choice == '0':
            break
        elif choice == '1':
            email = input('[?] Email to verify: ').strip()
            valid, msg = verify_email(email)
            status = f'{Fore.GREEN}Valid' if valid else f'{Fore.RED}Invalid'
            print(f'{status}: {msg}{Style.RESET_ALL}')
        elif choice == '2':
            sender = input('[?] Your email: ').strip()
            password = input('[?] App password: ').strip()
            recipient = input('[?] Recipient: ').strip()
            subject = input('[?] Subject: ').strip()
            body = input('[?] Body: ').strip()
            send_email(sender, password, recipient, subject, body)
        elif choice == '3':
            sender = input('[?] Your email: ').strip()
            password = input('[?] App password: ').strip()
            file_path = input('[?] Recipients file: ').strip()
            subject = input('[?] Subject: ').strip()
            body = input('[?] Body: ').strip()
            mass_email(sender, password, file_path, subject, body)
        elif choice == '4':
            generate_temp_email()
        elif choice == '5':
            username = input('[?] Username: ').strip()
            domain = input('[?] Domain: ').strip()
            check_inbox(username, domain)

if __name__ == '__main__':
    main()
