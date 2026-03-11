# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: 'phonenumber.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from colorama import Fore
import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime, UTC
def get_phone_info(phone_number):
    # ***<module>.get_phone_info: Failure: Different bytecode
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            input('Invalid')
            return
        country_code = f'+{parsed_number.country_code}' if parsed_number.country_code else 'None'
        operator = carrier.name_for_number(parsed_number, 'fr') or 'None'
        type_number = 'Mobile' if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE else 'Fixe'
        timezones = timezone.time_zones_for_number(parsed_number)
        timezone_info = timezones[0] if timezones else 'None'
        country = phonenumbers.region_code_for_number(parsed_number) or 'None'
        region = geocoder.description_for_number(parsed_number, 'fr') or 'None'
        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL) or 'None'
        status = 'Valid'
        print(f'\n[+] Status       : {status}\n[+] Formatted    : {formatted_number}\n[+] Country Code : {country_code}\n[+] Country      : {country}\n[+] Region       : {region}\n[+] Timezone     : {timezone_info}\n[+] Operator     : {operator}\n[+] Type Number  : {type_number}\n    ')
        input()
    except:
        print('[+] Invalid format !')
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

clear_screen()
print(Fore.GREEN, '\n                                                  \n                                 .                                \n                              .-+##+.                             \n                          ..=*%%%%%%#=.                           \n                     ...-*%%%@@%%#%%%%+:.                         \n                   .:+*%%%%%%%%%%*::#%%%*.                        \n                  .+%%%%##%%%*-=+=+::-%%%#+.                      \n                  .-%%%%%%=:=-+=*+:::::+%%%+-.                    \n                    :#@%%%%#**+=-::::::::#%%%*..                  \n                     .+%%%%%%*=:::::::::-=+%%%*+.                 \n                       :#%%%%%#::::::::=#%%%%%%+%=                \n                        .+%@#%%%=:--=%%%%%%%%%%%%%#.              \n                         ..#@%%%%%%%%%%%%%%##%##-+%%*.            \n                           .+%@#%%%%%%%%#+%%%#+%**#%%%=..         \n                            .:%@%++%%%#%*%%##%%%%%%%%#%#:.        \n                               +%@#%##=:##=++=%%%%%%@%%%%*.       \n                                :#@@%%###%%%%%#*#%%%%##@%%%=.     \n                                 .+%@%%%%%%#%%%%%%#%%%%*##%%#:.   \n                                   :%@%%##%%%%%*#%%%%%%%%%%##%#.. \n                                   .+%@%%*%*%%#%%*%@%%%%%%@%%%#. \n                                     .:#%@*%%%##%%%%#%*%%%%%%%#.. \n                                       .+%@%%#@%%%%%%@@%%%%#=..   \n                                        .:%%%%**%%@%@%%%%=...     \n                                          .*%@%%%%%%%#+..         \n                                            :#%@%%#+..            \n                                             ..--...                   \n')
tel = input('[+] Phone Number : ')
get_phone_info(tel)
