import os
import shutil
import time

os.system('color')

def MainColor(text):
    start_color = (30, 58, 138)
    end_color = (114, 14, 158)
    num_steps = 9
    colors = []
    
    for i in range(num_steps):
        r = start_color[0] + (end_color[0] - start_color[0]) * i // (num_steps - 1)
        g = start_color[1] + (end_color[1] - start_color[1]) * i // (num_steps - 1)
        b = start_color[2] + (end_color[2] - start_color[2]) * i // (num_steps - 1)
        colors.append((r, g, b))
    
    colors += list(reversed(colors[:-1]))
    
    def text_color(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"
    
    lines = text.split('\n')
    num_colors = len(colors)
    result = []
    
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if 1 == 1:
                color_index = (i + j) % num_colors
                color = colors[color_index]
                result.append(text_color(*color) + char + "\033[0m")
            else:
                result.append(char)
        if i < len(lines) - 1:
            result.append('\n')
    
    return ''.join(result)

def center_ascii(ascii_text):
    lines = ascii_text.split('\n')
    terminal_width = shutil.get_terminal_size().columns
    centered_lines = []
    
    for line in lines:
        if line.strip():
            padding = (terminal_width - len(line)) // 2
            centered_lines.append(' ' * padding + line)
        else:
            centered_lines.append(line)
    
    return '\n'.join(centered_lines)

ascii_art = r""" 
   ____    _     _____   _      ____   _       __  __      ____   U _____ u   
U /"___|U /"\ u |_ " _| U /"\ u U /"___| |"|      \ \ / //  __"| u\| ___"|/  
\| |  u \/ _ \/   | |   \/ _ \/  \| | u  U | | u    \ V /<\___ \/  |  _|"    
 | |/__ / ___ \  /| |\  / ___ \   | |/__  \| |/__  U_|"|_u ___) |   | |___   
  \____/_/   \_\u |_|U /_/   \_\   \____|  |_____|   |_|  |____/>>  |_____|  
  _// \\  \\    >> _// \\_\\    >>  _// \\   <<   >>.-,//|(_  )(   <<   >>   
 (__)(__)(__)  (__)(__)(__)  (__)(__)(__) (__) (__)\_) (__)(__)(__)(__) (__) 
 [ CRACKED ] This software has been cracked by Cataclyse ( Srungot )   """

additional_text = """

    Links:
        - https://udtrust.ovh
        - https://morose.nizzix.ovh
        - https://nizzix.xyz
        - https://github.com/srungot
        - https://git.udtrust.ovh
"""

os.system("cls")
print("\n")
print(MainColor(center_ascii(ascii_art)))
print(MainColor(additional_text))

os.system("start https://github.com/srungot")
import sys
import threading

for i in range(3, 0, -1):
    sys.stdout.write(f"\rLoading {i}.. ")
    sys.stdout.flush()
    threading.Event().wait(1)