"""
"""
import re
import json
import logging

from .urls import urls
from .session import Session
from .exceptions import WrongStatusCode, JsonLoadError, ProfitContentError

log = logging.getLogger(__name__)

class Profit(object):

    def __init__(self, symbol, session = None):
        self.symbol = symbol
        self.s = session if session else Session()
        self._profits = None
        self._simple = None

    def _update(self):
        self.s.touch()
        url = urls.profit(self.symbol)
        log.debug('request ' + url)
        resp = self.s.get(url)
        if resp.status_code != 200:
            raise WrongStatusCode(resp.status_code)
        try:
            data = json.loads(resp.text)
        except json.decoder.JSONDecodeError:
            raise JsonLoadError('"{}..."'.format(resp.text[:50]))
        return data
    
    def get(self, days = 0, origin = False, update = False):
        if update or self._profits is None:
            self._profits = self._update()
            self._simple = None
        if origin:
            return self._profits
        if self._simple is None:
            try:
                self._simple = [(int(re.sub('-', '', day['date'])), day['value']) for day in self._profits[0]['list']]
            except KeyError as e:
                raise ProfitContentError(str(e))
        if days:
            return self._simple[-int(days):]
        return self._simple
