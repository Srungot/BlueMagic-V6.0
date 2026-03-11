# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'discordtool.py'
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import customtkinter as ctk
import discord
from discord.ext import commands
import asyncio
import threading
import re
import sys

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def clone_server(source_guild_id, destination_guild_id, options, app):
    source = bot.get_guild(source_guild_id)
    dest = bot.get_guild(destination_guild_id)
    if not source or not dest:
        app.log('[ERROR] Source or destination server not found.')
        return None
    app.log(f'[INFO] Cloning server {source_guild_id} → {destination_guild_id}')
    
    if options.get('clone_roles', False):
        app.log('[INFO] Cloning roles...')
        roles_created = 0
        for role in sorted(source.roles, key=lambda r: r.position, reverse=True):
            if role.name != '@everyone':
                try:
                    await dest.create_role(name=role.name, permissions=role.permissions, colour=role.colour, hoist=role.hoist, mentionable=role.mentionable)
                    roles_created += 1
                except Exception as e:
                    app.log(f'[WARN] Could not clone role {role.name}: {e}')
        app.log(f'[INFO] {roles_created} roles cloned.')
    
    if options.get('clone_channels', False):
        app.log('[INFO] Cloning channels and categories...')
        category_map = {}
        categories_created = 0
        channels_created = 0
        for category in source.categories:
            try:
                new_cat = await dest.create_category(name=category.name, overwrites=category.overwrites)
                category_map[category.id] = new_cat
                categories_created += 1
            except Exception as e:
                app.log(f'[WARN] Could not clone category {category.name}: {e}')
        for channel in source.channels:
            try:
                if isinstance(channel, discord.TextChannel):
                    cat = category_map.get(channel.category_id)
                    await dest.create_text_channel(name=channel.name, category=cat, overwrites=channel.overwrites)
                    channels_created += 1
                elif isinstance(channel, discord.VoiceChannel):
                    cat = category_map.get(channel.category_id)
                    await dest.create_voice_channel(name=channel.name, category=cat, overwrites=channel.overwrites)
                    channels_created += 1
            except Exception as e:
                app.log(f'[WARN] Could not clone channel {channel.name}: {e}')
        app.log(f'[INFO] {categories_created} categories and {channels_created} channels cloned.')

async def raid_guild(guild_id, options, app):
    guild = bot.get_guild(guild_id)
    if guild is None:
        app.log(f'[ERROR] Server {guild_id} not found.')
        return None
    app.log(f'[INFO] Starting raid on server: {guild.name} ({guild.id})')
    
    channels_deleted = 0
    roles_deleted = 0
    members_kicked = 0
    members_banned = 0
    
    if options.get('delete_channels', False):
        app.log('[INFO] Deleting channels...')
        for channel in guild.channels:
            try:
                await channel.delete()
                channels_deleted += 1
            except Exception as e:
                pass
        app.log(f'[INFO] {channels_deleted} channels deleted.')
    
    if options.get('delete_roles', False):
        app.log('[INFO] Deleting roles...')
        for role in guild.roles:
            if role.name != '@everyone':
                try:
                    await role.delete()
                    roles_deleted += 1
                except Exception as e:
                    pass
        app.log(f'[INFO] {roles_deleted} roles deleted.')
    
    if options.get('kick_members', False):
        app.log('[INFO] Kicking members...')
        for member in guild.members:
            if member != bot.user:
                try:
                    await member.kick()
                    members_kicked += 1
                except Exception as e:
                    pass
        app.log(f'[INFO] {members_kicked} members kicked.')
    
    if options.get('ban_members', False):
        app.log('[INFO] Banning members...')
        for member in guild.members:
            if member != bot.user:
                try:
                    await member.ban()
                    members_banned += 1
                except Exception as e:
                    pass
        app.log(f'[INFO] {members_banned} members banned.')
    
    if options.get('spam_everyone', False):
        app.log('[INFO] Spamming @everyone...')
        spam_message = options.get('spam_message', '@everyone Raid!')
        for channel in guild.text_channels:
            try:
                for _ in range(5):
                    await channel.send(spam_message)
            except Exception as e:
                pass
    
    if options.get('create_channels', False):
        prefix = options.get('channel_prefix', 'raid')
        for i in range(10):
            try:
                channel = await guild.create_text_channel(name=f'{prefix}-{i}')
                await channel.send(options.get('channel_message', 'Raid!'))
            except Exception as e:
                pass

async def create_custom_channels(guild_id, channels, category_name, app):
    guild = bot.get_guild(guild_id)
    if guild is None:
        app.log('[ERROR] Server not found.')
        return None
    category = None
    if category_name:
        try:
            category = await guild.create_category(name=category_name)
        except Exception as e:
            app.log(f'[WARN] Could not create category: {e}')
    channels_created = 0
    for name in channels:
        try:
            await guild.create_text_channel(name=name, category=category)
            channels_created += 1
        except Exception as e:
            app.log(f'[WARN] Could not create channel {name}: {e}')
    app.log(f'[INFO] {channels_created} channels created.')

async def advanced_features(guild_id, options, app):
    guild = bot.get_guild(guild_id)
    if not guild:
        app.log('[ERROR] Server not found.')
        return None
    
    if options.get('mass_dm', False):
        app.log('[INFO] Sending mass DMs...')
        message = options.get('dm_message', 'Test message')
        dms_sent = 0
        for member in guild.members:
            if member != bot.user:
                try:
                    await member.send(message)
                    dms_sent += 1
                except Exception as e:
                    pass
        app.log(f'[INFO] {dms_sent} DMs sent.')
    
    if options.get('server_nuke', False):
        app.log('[INFO] Starting server nuke...')
        for channel in guild.channels:
            try:
                await channel.delete()
            except:
                pass
        for role in guild.roles:
            if role.name != '@everyone':
                try:
                    await role.delete()
                except:
                    pass
        app.log('[INFO] Server nuked.')

class DiscoSpliffApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('DiscoSpliff')
        self.geometry('550x600')
        self.resizable(False, False)
        self.configure(fg_color='#1C2526')
        main_frame = ctk.CTkFrame(self, fg_color='#1C2526', corner_radius=0)
        main_frame.pack(fill='both', expand=True)
        self.label = ctk.CTkLabel(main_frame, text='DiscoSpliff', font=('Arial', 18, 'bold'), text_color='#FF5555')
        self.label.pack(pady=10)
        self.tabview = ctk.CTkTabview(main_frame, width=500, height=300, corner_radius=8, fg_color='#2D3839', segmented_button_selected_color='#FF5555')
        self.tabview.pack(pady=10)
        self.tab_clone = self.tabview.add('Clone')
        self.tab_raid = self.tabview.add('Raid')
        self.tab_custom = self.tabview.add('Custom')
        self.tab_advanced = self.tabview.add('Advanced')
        
        # Clone tab
        self.clone_frame = ctk.CTkFrame(self.tab_clone, fg_color='#2D3839', corner_radius=8)
        self.clone_frame.pack(pady=10, padx=10, fill='both')
        self.clone_frame.grid_columnconfigure((0, 1), weight=1)
        self.source_entry = ctk.CTkEntry(self.clone_frame, placeholder_text='Source Guild ID', width=180, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.source_entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.dest_entry = ctk.CTkEntry(self.clone_frame, placeholder_text='Destination Guild ID', width=180, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.dest_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.clone_roles_var = ctk.BooleanVar(value=False)
        self.clone_channels_var = ctk.BooleanVar(value=False)
        self.clone_members_var = ctk.BooleanVar(value=False)
        self.assign_roles_var = ctk.BooleanVar(value=False)
        self.clone_roles_checkbox = ctk.CTkCheckBox(self.clone_frame, text='Clone Roles', variable=self.clone_roles_var, text_color='#FFFFFF')
        self.clone_roles_checkbox.grid(row=1, column=0, padx=5, pady=3, sticky='w')
        self.clone_channels_checkbox = ctk.CTkCheckBox(self.clone_frame, text='Clone Channels', variable=self.clone_channels_var, text_color='#FFFFFF')
        self.clone_channels_checkbox.grid(row=1, column=1, padx=5, pady=3, sticky='w')
        self.clone_button = ctk.CTkButton(self.clone_frame, text='Clone Server', command=self.clone_server, fg_color='#FF5555', hover_color='#FF7777', width=150, height=35)
        self.clone_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Raid tab
        self.raid_frame = ctk.CTkFrame(self.tab_raid, fg_color='#2D3839', corner_radius=8)
        self.raid_frame.pack(pady=10, padx=10, fill='both')
        self.raid_frame.grid_columnconfigure((0, 1), weight=1)
        self.raid_entry = ctk.CTkEntry(self.raid_frame, placeholder_text='Guild ID', width=360, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.raid_entry.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        self.delete_channels_var = ctk.BooleanVar(value=False)
        self.delete_roles_var = ctk.BooleanVar(value=False)
        self.kick_members_var = ctk.BooleanVar(value=False)
        self.ban_members_var = ctk.BooleanVar(value=False)
        self.spam_everyone_var = ctk.BooleanVar(value=False)
        self.create_channels_var = ctk.BooleanVar(value=False)
        self.delete_channels_checkbox = ctk.CTkCheckBox(self.raid_frame, text='Delete Channels', variable=self.delete_channels_var, text_color='#FFFFFF')
        self.delete_channels_checkbox.grid(row=1, column=0, padx=5, pady=3, sticky='w')
        self.delete_roles_checkbox = ctk.CTkCheckBox(self.raid_frame, text='Delete Roles', variable=self.delete_roles_var, text_color='#FFFFFF')
        self.delete_roles_checkbox.grid(row=1, column=1, padx=5, pady=3, sticky='w')
        self.kick_members_checkbox = ctk.CTkCheckBox(self.raid_frame, text='Kick Members', variable=self.kick_members_var, text_color='#FFFFFF')
        self.kick_members_checkbox.grid(row=2, column=0, padx=5, pady=3, sticky='w')
        self.ban_members_checkbox = ctk.CTkCheckBox(self.raid_frame, text='Ban Members', variable=self.ban_members_var, text_color='#FFFFFF')
        self.ban_members_checkbox.grid(row=2, column=1, padx=5, pady=3, sticky='w')
        self.spam_everyone_checkbox = ctk.CTkCheckBox(self.raid_frame, text='Spam @everyone', variable=self.spam_everyone_var, text_color='#FFFFFF')
        self.spam_everyone_checkbox.grid(row=3, column=0, padx=5, pady=3, sticky='w')
        self.raid_button = ctk.CTkButton(self.raid_frame, text='Launch Raid', command=self.raid_server, fg_color='#FF5555', hover_color='#FF7777', width=150, height=35)
        self.raid_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Custom tab
        self.custom_frame = ctk.CTkFrame(self.tab_custom, fg_color='#2D3839', corner_radius=8)
        self.custom_frame.pack(pady=10, padx=10, fill='both')
        self.custom_guild_entry = ctk.CTkEntry(self.custom_frame, placeholder_text='Guild ID', width=360, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.custom_guild_entry.pack(pady=5)
        self.channel_names_entry = ctk.CTkEntry(self.custom_frame, placeholder_text='Channel Names (comma-separated)', width=360, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.channel_names_entry.pack(pady=5)
        self.custom_button = ctk.CTkButton(self.custom_frame, text='Create Channels', command=self.create_custom_channels, fg_color='#FF5555', hover_color='#FF7777', width=150, height=35)
        self.custom_button.pack(pady=10)
        
        # Advanced tab
        self.adv_frame = ctk.CTkFrame(self.tab_advanced, fg_color='#2D3839', corner_radius=8)
        self.adv_frame.pack(pady=10, padx=10, fill='both')
        self.adv_guild_entry = ctk.CTkEntry(self.adv_frame, placeholder_text='Guild ID', width=360, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.adv_guild_entry.pack(pady=5)
        self.mass_dm_var = ctk.BooleanVar(value=False)
        self.server_nuke_var = ctk.BooleanVar(value=False)
        self.mass_dm_checkbox = ctk.CTkCheckBox(self.adv_frame, text='Mass DM', variable=self.mass_dm_var, text_color='#FFFFFF')
        self.mass_dm_checkbox.pack(pady=3, anchor='w')
        self.dm_message_entry = ctk.CTkEntry(self.adv_frame, placeholder_text='DM Message', width=360, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.dm_message_entry.pack(pady=5)
        self.server_nuke_checkbox = ctk.CTkCheckBox(self.adv_frame, text='Server Nuke', variable=self.server_nuke_var, text_color='#FFFFFF')
        self.server_nuke_checkbox.pack(pady=3, anchor='w')
        self.adv_button = ctk.CTkButton(self.adv_frame, text='Run Advanced', command=self.run_advanced, fg_color='#FF5555', hover_color='#FF7777', width=150, height=35)
        self.adv_button.pack(pady=10)
        
        # Token
        self.token_frame = ctk.CTkFrame(main_frame, fg_color='#1C2526', corner_radius=8)
        self.token_frame.pack(pady=10, padx=10, fill='x')
        self.token_entry = ctk.CTkEntry(self.token_frame, placeholder_text='Bot Token', width=360, height=30, fg_color='#3A4A4B', text_color='#FFFFFF', show='*')
        self.token_entry.pack(pady=5, padx=5)
        self.connect_button = ctk.CTkButton(self.token_frame, text='Connect', command=self.run_bot, fg_color='#00AA00', hover_color='#00CC00', width=150, height=35)
        self.connect_button.pack(pady=5)
        
        # Log
        self.log_textbox = ctk.CTkTextbox(main_frame, width=500, height=120, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.log_textbox.pack(pady=10, padx=10)
        self.log_textbox.configure(state='disabled')
        self.bot_loop = None
    
    def log(self, message):
        self.log_textbox.configure(state='normal')
        self.log_textbox.insert('end', message + '\n')
        self.log_textbox.see('end')
        self.log_textbox.configure(state='disabled')
    
    def clone_server(self):
        try:
            source_guild_id = int(self.source_entry.get())
            destination_guild_id = int(self.dest_entry.get())
            options = {'clone_roles': self.clone_roles_var.get(), 'clone_channels': self.clone_channels_var.get()}
            if self.bot_loop:
                asyncio.run_coroutine_threadsafe(clone_server(source_guild_id, destination_guild_id, options, self), self.bot_loop)
            else:
                self.log('[ERROR] Bot not connected.')
        except ValueError:
            self.log('[ERROR] Please enter valid Guild IDs.')
    
    def raid_server(self):
        try:
            guild_id = int(self.raid_entry.get())
            options = {
                'delete_channels': self.delete_channels_var.get(),
                'delete_roles': self.delete_roles_var.get(),
                'kick_members': self.kick_members_var.get(),
                'ban_members': self.ban_members_var.get(),
                'spam_everyone': self.spam_everyone_var.get()
            }
            if self.bot_loop:
                asyncio.run_coroutine_threadsafe(raid_guild(guild_id, options, self), self.bot_loop)
            else:
                self.log('[ERROR] Bot not connected.')
        except ValueError:
            self.log('[ERROR] Please enter a valid Guild ID.')
    
    def create_custom_channels(self):
        try:
            guild_id = int(self.custom_guild_entry.get())
            channel_names = [name.strip() for name in self.channel_names_entry.get().split(',') if name.strip()]
            if self.bot_loop:
                asyncio.run_coroutine_threadsafe(create_custom_channels(guild_id, channel_names, None, self), self.bot_loop)
            else:
                self.log('[ERROR] Bot not connected.')
        except ValueError:
            self.log('[ERROR] Please enter a valid Guild ID.')
    
    def run_advanced(self):
        try:
            guild_id = int(self.adv_guild_entry.get())
            options = {
                'mass_dm': self.mass_dm_var.get(),
                'dm_message': self.dm_message_entry.get() or 'Test message',
                'server_nuke': self.server_nuke_var.get()
            }
            if self.bot_loop:
                asyncio.run_coroutine_threadsafe(advanced_features(guild_id, options, self), self.bot_loop)
            else:
                self.log('[ERROR] Bot not connected.')
        except ValueError:
            self.log('[ERROR] Please enter a valid Guild ID.')
    
    def run_bot(self):
        token = self.token_entry.get().strip()
        if not token:
            self.log('[ERROR] Please enter a valid token.')
            return
        self.log('[INFO] Attempting to connect bot...')
        self.connect_button.configure(state='disabled')
        threading.Thread(target=self._start_bot_thread, args=(token,), daemon=True).start()
    
    def _start_bot_thread(self, token):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.bot_loop = loop
        try:
            loop.run_until_complete(bot.start(token))
        except discord.errors.LoginFailure:
            self.log('[ERROR] Invalid token.')
            self.connect_button.configure(state='normal')
        except Exception as e:
            self.log(f'[ERROR] Bot connection failed: {e}')
            self.connect_button.configure(state='normal')

@bot.event
async def on_ready():
    print(f'[INFO] Bot ready as {bot.user}')

def main():
    app = DiscoSpliffApp()
    app.mainloop()

if __name__ == '__main__':
    main()
