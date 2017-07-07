"""
"""
import re
import hashlib
import logging
import requests
from requests.cookies import RequestsCookieJar

from .urls import urls
from .headers import default_headers
from .exceptions import LoginError

log = logging.getLogger(__name__)

class Session(requests.Session):

    def __init__(self):
        super(Session, self).__init__()
        self.headers = default_headers()

    def touch(self):
        if 'xq_a_token' not in self.cookies:
            log.debug('touch ' + urls.base)
            self.get(urls.base)

    def is_login(self):
        return 'xq_a_token' in self.cookies and 'xq_r_token' in self.cookies and 'xq_is_login' in self.cookies
    
    def login(self, username, password):
        self.cookies = RequestsCookieJar()
        self.touch()
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        if re.search('^[\d]+$', username):
            data = {'areacode': 86, 'telephone': username, 'password': password, 'remember_me': 'on'}
        else:
            data = {'username': username, 'password': password}
        log.debug('login ' + urls.login)
        resp = self.post(urls.login, data = data)
        if not self.is_login():
            raise LoginError('http code: {}'.format(resp.status_code))
