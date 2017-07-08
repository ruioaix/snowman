"""
"""
import os
import re
import json
import hashlib
import logging
import getpass
import requests
from requests.cookies import RequestsCookieJar
from requests.utils import dict_from_cookiejar, cookiejar_from_dict

from .urls import urls
from .headers import default_headers
from .exceptions import LoginError

log = logging.getLogger(__name__)

class Session(requests.Session):

    def __init__(self):
        super(Session, self).__init__()
        self.headers = default_headers()
        self.file_login_cookies = '.snowman_login_cookies'
        self.file_anony_cookies = '.snowman_anony_cookies'

    def touch(self):
        if 'xq_a_token' not in self.cookies:
            self.read_anony_cookies()
            if 'xq_a_token' not in self.cookies:
                log.debug('touch ' + urls.base)
                self.get(urls.base)
                self.save_cookies()

    def login(self, username, password):
        self.cookies = RequestsCookieJar()
        log.debug('before login, first visit ' + urls.base)
        self.get(urls.base)
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        if re.search('^[\d]+$', username):
            data = {'areacode': 86, 'telephone': username, 'password': password, 'remember_me': 'on'}
        else:
            data = {'username': username, 'password': password}
        log.debug('login with ' + username + ' via ' + urls.login)
        resp = self.post(urls.login, data = data)
        if not self.is_login():
            raise LoginError(username + ' login failed.')
        self.save_cookies()

    def is_login(self):
        return ('u' in self.cookies and
                'xq_a_token' in self.cookies and 
                'xq_r_token' in self.cookies and 
                'xq_is_login' in self.cookies and
                self.cookies['xq_is_login'] == '1')
    
    def be_login(self):
        if not self.is_login():
            self.read_login_cookies()
            if not self.is_login():
                username = input("username: ")
                password = getpass.getpass()
                self.login(username, password)

    def save_cookies(self):
        if self.is_login():
            fp = os.path.join(os.path.expanduser('~'), self.file_login_cookies)
        else:
            fp = os.path.join(os.path.expanduser('~'), self.file_anony_cookies)
        with open(fp, 'w') as fo:
            json.dump(dict_from_cookiejar(self.cookies), fo)

    def _read_cookies(self, login = True):
        fp = os.path.join(os.path.expanduser('~'), self.file_login_cookies if login else self.file_anony_cookies)
        if os.path.exists(fp):
            with open(fp) as fo:
                self.cookies = cookiejar_from_dict(json.load(fo))

    def read_login_cookies(self):
        self._read_cookies()

    def read_anony_cookies(self):
        self._read_cookies(False)

