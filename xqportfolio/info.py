"""
"""
import re
import json
import datetime

import requests

from . import urls
from .headers import default_headers

class Info(object):

    def __init__(self, symbol):
        self.symbol = symbol
        self.info = None

    def _update(self):
        with requests.Session() as s:
            resp = s.get(urls.info(self.symbol), headers = default_headers())
            #cubeinfo = re.sub("[\s\S]*SNB.cubeInfo[\s]*=[\s]*", '', str(resp.text))
            #cubeinfo = re.sub(";[\s]*SNB.cubePieData[\s]*=[\s\S]*", '', str(cubeinfo))
            cubeinfo = re.search(r'(?<=SNB.cubeInfo = ).*(?=;[\s]SNB.cubePieData)', resp.text)
            if cubeinfo is None: 
                raise Exception("Info can not be found from url: '{}'".format(urls.info(self.symbol)))
            try:
                data = json.loads(cubeinfo.group())
            except json.decoder.JSONDecodeError:
                raise Exception('Json loads error')
            self.info = data

    def all(self, update = False):
        if update or not self.info: 
            self._update()
        return self.info

    def basic(self, update = False):
        if update or not self.info:
            self._update()
        res = {'symbol': self.symbol}
        res['name'] = self.info['name']
        res['market'] = self.info['market']
        res['status'] = 'active' if self.info['active_flag'] else 'closed'
        res['created'] = self.info['created_date']
        updated_at = datetime.datetime.fromtimestamp(self.info['updated_at'] // 1000)
        res['updated_at'] = updated_at.strftime('%Y-%m-%d %H:%M:%S')
        res['net_value'] = self.info['net_value']
        res['follower_count'] = self.info['follower_count']
        return res

    def __getattr__(self, name):
        if name in self.info:
            return self.info[name]
        raise AttributeError("'{}' object has no attribut '{}'".format(Info.__name__, name))
