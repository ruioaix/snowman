"""
"""
import re
import json

from .urls import urls
from .session import Session

class Profit(object):

    def __init__(self, symbol, session = None):
        self.symbol = symbol
        self.s = session if session else Session()
        self._profits = None
        self._simple = None

    def _update(self):
        self.s.touch()
        resp = self.s.get(urls.profit(self.symbol))
        try:
            data = json.loads(resp.text)
        except json.decoder.JSONDecodeError:
            raise Exception('Json loads error: {}'.format(resp.text[:50]))
        return data
    
    def get(self, days = 0, origin = False, update = False):
        if update or self._profits is None:
            self._profits = self._update()
            self._simple = None
        if origin:
            return self._profits
        if self._simple is None:
            self._simple = [(int(re.sub('-', '', day['date'])), day['value']) for day in self._profits[0]['list']]
        if days:
            return self._simple[-int(days):]
        return self._simple
