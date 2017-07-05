"""
"""
import re
import json
import datetime

from .urls import urls
from .session import Session

class Info(object):

    def __init__(self, symbol, session = None):
        self.symbol = symbol
        self.s = session if session else Session()
        self._info = None
        self._simple = None

    def __getattr__(self, name):
        if name in self._info:
            return self._info[name]
        raise AttributeError("'{}' object has no attribut '{}'".format(Info.__name__, name))

    def _update(self):
        resp = self.s.get(urls.info(self.symbol))
        cubeinfo = re.search(r'(?<=SNB.cubeInfo = ).*(?=;[\s]SNB.cubePieData)', resp.text)
        if cubeinfo is None: 
            raise Exception("Info can not be found from url: '{}'".format(urls.info(self.symbol)))
        try:
            data = json.loads(cubeinfo.group())
        except json.decoder.JSONDecodeError:
            raise Exception('Json loads error')
        return data

    def get(self, origin = False, update = False):
        if update or self._info is None: 
            self._info = self._update()
            self._simple = None
        if origin: 
            return self._info
        if self._simple is None:
            self._simple = {'symbol': self.symbol}
            self._simple['name'] = self._info['name']
            self._simple['market'] = self._info['market']
            self._simple['status'] = 'active' if self._info['active_flag'] else 'closed'
            self._simple['created'] = self._info['created_date']
            updated_at = datetime.datetime.fromtimestamp(self._info['updated_at'] // 1000)
            self._simple['updated_at'] = updated_at.strftime('%Y-%m-%d %H:%M:%S')
            self._simple['net_value'] = self._info['net_value']
            self._simple['follower_count'] = self._info['follower_count']
        return self._simple
