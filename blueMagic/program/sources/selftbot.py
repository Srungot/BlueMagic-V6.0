# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'selftbot.py'
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import requests
import threading
import time
import random
import json
import os
import concurrent.futures
from PIL import Image, ImageTk, ImageDraw
import io
import base64

API_BASE = 'https://discord.com/api/v9'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131.0.0.0'}

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

TRANSLATIONS = {
    'fr': {
        'app_title': 'BluCore - v1.0 Premium',
        'dashboard': 'Tableau de bord',
        'auto_reply': 'Réponse Auto',
        'status_rpc': 'Statut & RPC',
        'dm_friends': 'MP & Amis',
        'scripts': 'Scripts',
        'settings': 'Paramètres',
        'connect_token': 'Connecter Token',
        'token_empty': 'Token vide',
        'token_invalid': 'Token invalide',
        'connected': 'Connecté !',
        'uptime': 'Uptime'
    }
}

PRESET_COLORS = {
    'Rouge Vif': '#ef4444',
    'Orange Solaire': '#f97316',
    'Jaune Or': '#eab308',
    'Vert Émeraude': '#10b981',
    'Bleu Ciel': '#0ea5e9',
    'Bleu Roi': '#3b82f6',
    'Indigo Profond': '#6366f1',
    'Violet Mystique': '#8b5cf6',
    'Rose Bonbon': '#ec4899',
    'Cyan Futuriste': '#06b6d4',
    'Blanc Pur': '#ffffff',
    'Gris Anthracite': '#1f2937',
    'Noir Profond': '#000000',
    'Nuit Sombre': '#0d001a',
    'Violet Nuit': '#050010',
    'Lavande': '#a78bfa',
    'Pourpre': '#4c1d95'
}

class NightyUltimateSelfBot(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.load_config()
        self.title(self.t('app_title'))
        self.geometry('1100x700')
        self.resizable(False, False)
        
        self.token = ''
        self.headers = HEADERS.copy()
        self.user_data = {}
        self.my_id = None
        self.username = 'BluCore'
        self.discriminator = '0001'
        self.avatar_url = 'https://cdn.discordapp.com/embed/avatars/0.png'
        self.nitro = False
        self.servers_count = 0
        self.friends_count = 0
        self.uptime_start = time.time()
        self.commands_used = 0
        
        self.configure(fg_color=self.colors['bg_color'])
        
        self.triggers = ['salut', 'cc', 'yo']
        self.responses = ['yo bg ça va ?', 'cc', 'quoi de neuf']
        self.auto_response_text = 'yo bg ça va ?'
        self.auto_reply_active = False
        self.running = False
        self.notifications = []
        
        self.build_ui()
        self.protocol('WM_DELETE_WINDOW', self.on_close)
        threading.Thread(target=self.update_uptime, daemon=True).start()

    def load_config(self):
        self.config_file = os.path.join('input', 'config.json')
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except:
                self.config = {}
        else:
            self.config = {}
        
        self.lang = self.config.get('language', 'fr')
        default_theme = {
            'bg_color': '#0d001a',
            'fg_color': '#ffffff',
            'sidebar_color': '#050010',
            'accent_color': '#a78bfa',
            'border_color': '#4c1d95',
            'text_color': '#c084fc',
            'secondary_text_color': '#94a3b8'
        }
        self.colors = self.config.get('theme', default_theme)
        for k, v in default_theme.items():
            if k not in self.colors:
                self.colors[k] = v

    def save_config(self):
        self.config['language'] = self.lang
        self.config['theme'] = self.colors
        os.makedirs('input', exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)

    def t(self, key):
        return TRANSLATIONS.get(self.lang, TRANSLATIONS['fr']).get(key, key)

    def build_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.main_frame = ctk.CTkFrame(self, fg_color=self.colors['bg_color'])
        self.main_frame.pack(fill='both', expand=True)
        
        self.sidebar = ctk.CTkFrame(self.main_frame, fg_color=self.colors['sidebar_color'], width=280, corner_radius=0)
        self.sidebar.pack(side='left', fill='y')
        
        logo = ctk.CTkLabel(self.sidebar, text='BluCore', font=('Montserrat', 42, 'bold'), text_color=self.colors['accent_color'])
        logo.pack(pady=(60, 5))
        
        version = ctk.CTkLabel(self.sidebar, text='v1.0 BluCore', font=('Roboto', 12), text_color=self.colors['secondary_text_color'])
        version.pack(pady=(0, 40))
        
        menu = [
            ('📊 ' + self.t('dashboard'), self.show_dashboard),
            ('🤖 ' + self.t('auto_reply'), self.show_auto_reply),
            ('🎮 ' + self.t('status_rpc'), self.show_status_rpc),
            ('👥 ' + self.t('dm_friends'), self.show_dm_friends),
            ('📜 ' + self.t('scripts'), self.show_scripts),
            ('⚙️ ' + self.t('settings'), self.show_settings)
        ]
        
        for text, cmd in menu:
            btn = ctk.CTkButton(self.sidebar, text=text, font=('Roboto Medium', 14),
                fg_color='transparent', hover_color=self.colors['border_color'],
                text_color=self.colors['fg_color'], anchor='w', corner_radius=25,
                height=50, command=cmd)
            btn.pack(fill='x', padx=15, pady=5)
        
        self.content = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.content.pack(side='left', fill='both', expand=True, padx=40, pady=30)
        
        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        
        # User card
        user_card = ctk.CTkFrame(self.content, fg_color=self.colors['sidebar_color'],
            corner_radius=20, border_width=1, border_color=self.colors['border_color'])
        user_card.pack(fill='x', pady=(0, 20))
        
        info_frame = ctk.CTkFrame(user_card, fg_color='transparent')
        info_frame.pack(fill='x', padx=20, pady=20)
        
        self.username_label = ctk.CTkLabel(info_frame, text=f'{self.username}#{self.discriminator}',
            font=('Arial', 22, 'bold'), text_color=self.colors['fg_color'])
        self.username_label.pack(anchor='w')
        
        self.id_label = ctk.CTkLabel(info_frame, text=f"User ID: {self.my_id or 'Not Connected'}",
            font=('Arial', 12), text_color=self.colors['secondary_text_color'])
        self.id_label.pack(anchor='w')
        
        # Stats
        stats_frame = ctk.CTkFrame(user_card, fg_color='transparent')
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        ctk.CTkLabel(stats_frame, text=str(self.servers_count), font=('Arial', 20, 'bold'),
            text_color=self.colors['accent_color']).pack(side='left', padx=20)
        ctk.CTkLabel(stats_frame, text='SERVERS', font=('Arial', 10),
            text_color=self.colors['secondary_text_color']).pack(side='left')
        
        ctk.CTkLabel(stats_frame, text=str(self.friends_count), font=('Arial', 20, 'bold'),
            text_color=self.colors['accent_color']).pack(side='left', padx=20)
        ctk.CTkLabel(stats_frame, text='FRIENDS', font=('Arial', 10),
            text_color=self.colors['secondary_text_color']).pack(side='left')
        
        # Token entry
        token_frame = ctk.CTkFrame(self.content, fg_color=self.colors['sidebar_color'],
            corner_radius=20, border_width=1, border_color=self.colors['border_color'])
        token_frame.pack(fill='x', pady=0)
        
        ctk.CTkLabel(token_frame, text='Quick Connect', font=('Arial', 14, 'bold'),
            text_color=self.colors['text_color']).pack(anchor='w', padx=20, pady=(15, 5))
        
        self.token_entry = ctk.CTkEntry(token_frame, show='•', placeholder_text='Token here...',
            height=35, fg_color=self.colors['bg_color'], border_color=self.colors['border_color'])
        self.token_entry.pack(fill='x', padx=20, pady=5)
        
        ctk.CTkButton(token_frame, text='Connect', command=self.connect_token,
            fg_color=self.colors['accent_color'], hover_color=self.colors['border_color'],
            corner_radius=20).pack(fill='x', padx=20, pady=(5, 15))
        
        # Uptime
        self.uptime_label = ctk.CTkLabel(self.content, text='Uptime: 00:00:00',
            font=('Consolas', 12), text_color=self.colors['secondary_text_color'])
        self.uptime_label.pack(anchor='e', pady=10)

    def show_auto_reply(self):
        self.clear_content()
        
        card = ctk.CTkFrame(self.content, fg_color=self.colors['sidebar_color'],
            corner_radius=20, border_width=2, border_color=self.colors['border_color'])
        card.pack(fill='both', expand=True, pady=20, padx=20)
        
        title = ctk.CTkLabel(card, text=self.t('auto_reply'), font=('Consolas', 24, 'bold'),
            text_color=self.colors['text_color'])
        title.pack(pady=15)
        
        # Triggers
        triggers_frame = ctk.CTkFrame(card, fg_color='transparent')
        triggers_frame.pack(pady=10, padx=30, fill='x')
        
        ctk.CTkLabel(triggers_frame, text='Triggers (one per line):',
            text_color=self.colors['secondary_text_color']).pack(anchor='w')
        
        self.triggers_list = ctk.CTkTextbox(triggers_frame, height=80, text_color=self.colors['fg_color'])
        self.triggers_list.pack(pady=5, fill='x')
        self.triggers_list.insert('0.0', '\n'.join(self.triggers))
        
        # Response
        resp_frame = ctk.CTkFrame(card, fg_color='transparent')
        resp_frame.pack(pady=10, padx=30, fill='x')
        
        ctk.CTkLabel(resp_frame, text='Response:', text_color=self.colors['secondary_text_color']).pack(anchor='w')
        
        self.response_entry = ctk.CTkEntry(resp_frame, height=35, text_color=self.colors['fg_color'])
        self.response_entry.pack(pady=5, fill='x')
        self.response_entry.insert(0, self.auto_response_text)
        
        # Toggle button
        self.toggle_btn = ctk.CTkButton(card, text='Start Auto Reply',
            command=self.toggle_auto_reply, fg_color=self.colors['accent_color'],
            hover_color=self.colors['border_color'], corner_radius=20)
        self.toggle_btn.pack(pady=20)

    def show_status_rpc(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text=self.t('status_rpc'), font=('Arial', 24, 'bold'),
            text_color=self.colors['text_color']).pack(pady=20)

    def show_dm_friends(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text=self.t('dm_friends'), font=('Arial', 24, 'bold'),
            text_color=self.colors['text_color']).pack(pady=20)

    def show_scripts(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text=self.t('scripts'), font=('Arial', 24, 'bold'),
            text_color=self.colors['text_color']).pack(pady=20)

    def show_settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text=self.t('settings'), font=('Arial', 24, 'bold'),
            text_color=self.colors['text_color']).pack(pady=20)

    def toggle_auto_reply(self):
        self.auto_reply_active = not self.auto_reply_active
        if self.auto_reply_active:
            self.toggle_btn.configure(text='Stop Auto Reply', fg_color='#ef4444')
            self.log_msg('Auto Reply: ON', 'success')
        else:
            self.toggle_btn.configure(text='Start Auto Reply', fg_color=self.colors['accent_color'])
            self.log_msg('Auto Reply: OFF', 'info')

    def connect_token(self):
        self.token = self.token_entry.get().strip()
        if not self.token:
            messagebox.showerror('Erreur', self.t('token_empty'))
            return
        
        self.headers['Authorization'] = self.token
        try:
            r = requests.get(f'{API_BASE}/users/@me', headers=self.headers, timeout=6)
            if r.status_code == 200:
                self.user_data = r.json()
                self.my_id = self.user_data.get('id')
                self.username = self.user_data.get('username', 'BluCore')
                self.discriminator = self.user_data.get('discriminator', '0001')
                self.log_msg(self.t('connected'), 'success')
                self.load_guilds_and_friends()
                self.show_dashboard()
            else:
                messagebox.showerror('Erreur', self.t('token_invalid'))
        except Exception as e:
            self.log_msg(f"Connection error: {e}", 'error')

    def load_guilds_and_friends(self):
        try:
            r = requests.get(f'{API_BASE}/users/@me/guilds', headers=self.headers, timeout=6)
            if r.status_code == 200:
                self.servers_count = len(r.json())
        except:
            pass
        
        try:
            r = requests.get(f'{API_BASE}/users/@me/relationships', headers=self.headers, timeout=6)
            if r.status_code == 200:
                friends = [rel for rel in r.json() if rel['type'] == 1]
                self.friends_count = len(friends)
        except:
            pass

    def log_msg(self, msg, level='info'):
        self.notifications.append(f"[{level.upper()}] {msg}")
        print(f"[{level.upper()}] {msg}")

    def update_uptime(self):
        while True:
            try:
                elapsed = int(time.time() - self.uptime_start)
                hours = elapsed // 3600
                mins = elapsed % 3600 // 60
                secs = elapsed % 60
                if hasattr(self, 'uptime_label'):
                    self.uptime_label.configure(text=f"{self.t('uptime')}: {hours:02d}:{mins:02d}:{secs:02d}")
            except:
                pass
            time.sleep(1)

    def on_close(self):
        self.save_config()
        self.destroy()

if __name__ == '__main__':
    app = NightyUltimateSelfBot()
    app.mainloop()
