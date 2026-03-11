# Decompiled with PyLingual cmd version ( https://nizzix.xyz )
# Internal filename: keyauth.py
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import os
import json as jsond
import time
import binascii
import platform
import subprocess
import qrcode
from datetime import datetime, timezone, timedelta
from discord_interactions import verify_key
from PIL import Image
try:
    if os.name == 'nt':
        import win32security
    import requests
except ImportError:
    pass

class api:
    name = ownerid = version = hash_to_check = ''

    def __init__(self, name, ownerid, version, hash_to_check):
        if len(ownerid)!= 10:
            print('Visit https://keyauth.cc/app/, copy Pthon code, and replace code in main.py with that')
            time.sleep(3)
            os._exit(1)
        self.name = name
        self.ownerid = ownerid
        self.version = version
        self.hash_to_check = hash_to_check
        self.init()
    sessionid = enckey = ''
    initialized = False

    def init(self):
        if self.sessionid!= '':
            print('You\'ve already initialized!')
            time.sleep(3)
            os._exit(1)
        post_data = {'type': 'init', 'ver': self.version, 'hash': self.hash_to_check, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        if response == 'KeyAuth_Invalid':
            print('The application doesn\'t exist')
            time.sleep(3)
            os._exit(1)
        json = jsond.loads(response)
        if json['message'] == 'invalidver':
            if json['download']!= '':
                print('New Version Available')
                download_link = json['download']
                os.system(f'start {download_link}')
                time.sleep(3)
                os._exit(1)
        if not json['success']:
            print(json['message'])
            time.sleep(3)
            os._exit(1)
        self.sessionid = json['sessionid']
        self.initialized = True

    def register(self, user, password, license, hwid=None):
        self.checkinit()
        hwid = others.get_hwid() if hwid is None else hwid
        post_data = {'type': 'register', 'username': user, 'pass': password, 'key': license, 'hwid': hwid, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            print(json['message'])
            self.__load_user_data(json['info'])
        return None

    def upgrade(self, user, license):
        self.checkinit()
        post_data = {'type': 'upgrade', 'username': user, 'key': license, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            print(json['message'])
            print('Please restart program and login')
            time.sleep(3)
            os._exit(1)
        return None

    def login(self, user, password, code=None, hwid=None):
        self.checkinit()
        hwid = others.get_hwid() if hwid is None else hwid
        post_data = {'type': 'login', 'username': user, 'pass': password, 'hwid': hwid, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        if code is not None:
            post_data['code'] = code
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            self.__load_user_data(json['info'])
            print(json['message'])
        return None

    def license(self, key, code=None, hwid=None):
        self.checkinit()
        hwid = others.get_hwid() if hwid is None else hwid
        post_data = {'type': 'license', 'key': key, 'hwid': hwid, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        if code is not None:
            post_data['code'] = code
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            self.__load_user_data(json['info'])
            print(json['message'])
        return None

    def var(self, name):
        self.checkinit()
        post_data = {'type': 'var', 'varid': name, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        return json['message'] if json['success'] else None

    def getvar(self, var_name):
        self.checkinit()
        post_data = {'type': 'getvar', 'var': var_name, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        return json['response'] if json['success'] else None

    def setvar(self, var_name, var_data):
        self.checkinit()
        post_data = {'type': 'setvar', 'var': var_name, 'data': var_data, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            pass  # postinserted
        return True

    def ban(self):
        self.checkinit()
        post_data = {'type': 'ban', 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            pass  # postinserted
        return True

    def file(self, fileid):
        self.checkinit()
        post_data = {'type': 'file', 'fileid': fileid, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if not json['success']:
            print(json['message'])
            time.sleep(3)
            os._exit(1)
        return binascii.unhexlify(json['contents'])

    def webhook(self, webid, param, body='', conttype=''):
        self.checkinit()
        post_data = {'type': 'webhook', 'webid': webid, 'params': param, 'body': body, 'conttype': conttype, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            return json['message']

    def check(self):
        self.checkinit()
        post_data = {'type': 'check', 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            pass  # postinserted
        return True

    def checkblacklist(self):
        self.checkinit()
        hwid = others.get_hwid()
        post_data = {'type': 'checkblacklist', 'hwid': hwid, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            pass  # postinserted
        return True

    def log(self, message):
        self.checkinit()
        post_data = {'type': 'log', 'pcuser': os.getenv('username'), 'message': message, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        self.__do_request(post_data)

    def fetchOnline(self):
        self.checkinit()
        post_data = {'type': 'fetchOnline', 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success'] and len(json['users']) == 0:
            return None

    def fetchStats(self):
        self.checkinit()
        post_data = {'type': 'fetchStats', 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            self.__load_app_data(json['appinfo'])
        return None

    def chatGet(self, channel):
        self.checkinit()
        post_data = {'type': 'chatget', 'channel': channel, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            return json['messages']

    def chatSend(self, message, channel):
        self.checkinit()
        post_data = {'type': 'chatsend', 'message': message, 'channel': channel, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            pass  # postinserted
        return True

    def checkinit(self):
        if not self.initialized:
            print('Initialize first, in order to use the functions')
            time.sleep(3)
            os._exit(1)
        return None

    def changeUsername(self, username):
        self.checkinit()
        post_data = {'type': 'changeUsername', 'newUsername': username, 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            print('Successfully changed username')
        return None

    def logout(self):
        self.checkinit()
        post_data = {'type': 'logout', 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            print('Successfully logged out')
            time.sleep(3)
            os._exit(1)
        return None

    def enable2fa(self, code=None):
        self.checkinit()
        post_data = {'type': '2faenable', 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid, 'code': code}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        if json['success']:
            if code is None:
                print("Your 2FA secret code is: {json['2fa']['secret_code']}")
                qr_code = json['2fa']['QRCode']
                self.display_qr_code(qr_code)
                code_input = input('Enter the 6 digit 2fa code to enable 2fa: ')
                self.enable2fa(code_input)
            return None
        return None

    def disable2fa(self, code=None):
        self.checkinit()
        code = input('Enter the 6 digit 2fa code to disable 2fa: ')
        post_data = {'type': '2fadisable', 'sessionid': self.sessionid, 'name': self.name, 'ownerid': self.ownerid, 'code': code}
        response = self.__do_request(post_data)
        json = jsond.loads(response)
        print(json['message'])
        time.sleep(3)

    def display_qr_code(self, qr_code_url):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_code_url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.show()

    def __do_request(self, post_data):
        try:
            response = requests.post('https://keyauth.win/api/1.3/', data=post_data, timeout=10)
            if not (post_data['type'] == 'log' or post_data['type'] == 'file'):
                if post_data['type'] == '2faenable' or post_data['type'] == '2fadisable':
                    pass
            return response.text
        except requests.exceptions.Timeout:
            print('Request timed out. Server is probably down/slow at the moment')
            return 'KeyAuth_Invalid'

    class application_data_class:
        numUsers = numKeys = app_ver = customer_panel = onlineUsers = ''

    class user_data_class:
        username = ip = hwid = expires = createdate = lastlogin = subscription = subscriptions = ''
    user_data = user_data_class()
    app_data = application_data_class()

    def __load_app_data(self, data):
        self.app_data.numUsers = data['numUsers']
        self.app_data.numKeys = data['numKeys']
        self.app_data.app_ver = data['version']
        self.app_data.customer_panel = data['customerPanelLink']
        self.app_data.onlineUsers = data['numOnlineUsers']

    def __load_user_data(self, data):
        self.user_data.username = data['username']
        self.user_data.ip = data['ip']
        self.user_data.hwid = data['hwid'] or 'N/A'
        self.user_data.expires = data['subscriptions'][0]['expiry']
        self.user_data.createdate = data['createdate']
        self.user_data.lastlogin = data['lastlogin']
        self.user_data.subscription = data['subscriptions'][0]['subscription']
        self.user_data.subscriptions = data['subscriptions']

class others:
    @staticmethod
    def get_hwid():
        if platform.system() == 'Linux':
            with open('/etc/machine-id') as f:
                hwid = f.read()
                return hwid
        # Windows HWID
