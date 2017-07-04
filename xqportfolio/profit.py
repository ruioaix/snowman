"""
"""
import re
import copy
import json
import requests

from .urls import urls
from .headers import default_headers

class Profit(object):

    def __init__(self, symbol):
        self.symbol = symbol
        self._profits = None
        self._simple = None

    def _update(self):
        with requests.Session() as s:
            s.headers = default_headers()
            s.get(urls.base)
            resp = s.get(urls.profit(self.symbol))
            try:
                data = json.loads(resp.text)
            except json.decoder.JSONDecodeError:
                raise Exception('Json loads error: {}'.format(resp.text[:50]))
            self._profits = data
    
    def origin(self, update = False):
        if update or self._profits is None:
            self._update()
        return copy.deepcopy(self._profits)

    def simple(self, days = 0, update = False):
        if update or self._profits is None:
            self._update()
            self._simple = None
        if self._simple is None:
            self._simple = [(int(re.sub('-', '', day['date'])), day['value']) for day in self._profits[0]['list']]
        if days:
            return self._simple[-int(days):]
        return self._simple
