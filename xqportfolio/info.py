"""
"""
import re
import copy
import json
import datetime

import requests

from .urls import urls
from .headers import default_headers

class Info(object):

    def __init__(self, symbol):
        self.symbol = symbol
        self._info = None

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
            self._info = data

    def all(self, update = False):
        if update or not self._info: 
            self._update()
        return copy.deepcopy(self._info)

    def basic(self, update = False):
        if update or not self._info:
            self._update()
        res = {'symbol': self.symbol}
        res['name'] = self._info['name']
        res['market'] = self._info['market']
        res['status'] = 'active' if self._info['active_flag'] else 'closed'
        res['created'] = self._info['created_date']
        updated_at = datetime.datetime.fromtimestamp(self._info['updated_at'] // 1000)
        res['updated_at'] = updated_at.strftime('%Y-%m-%d %H:%M:%S')
        res['net_value'] = self._info['net_value']
        res['follower_count'] = self._info['follower_count']
        return res

    def __getattr__(self, name):
        if name in self._info:
            return self._info[name]
        raise AttributeError("'{}' object has no attribut '{}'".format(Info.__name__, name))

