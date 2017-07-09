"""
snowman.Profit
~~~~~~~~~~~~

This module provides a Profit object to get profit history of the portfolios 
on xueqiu.com
"""
import re
import json
import logging

from .urls import urls
from .session import Session
from .exceptions import WrongStatusCode, JsonLoadError, ProfitContentError

log = logging.getLogger(__name__)

class Profit(object):
    """ the profit history of a portfolio. 

    :param symbol: the portfolio symbol, a string starting with 'ZH'
    :param session: (optional) the session object responsible for http(s) connection 

    Usage::

    >>> from snowman import Profit
    >>> pft = Profit('ZH123456')
    >>> pft.get() # return all the profit history
    >>> pft.get(10) # return the profit history in the latest 10 days.

    """

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
    
    def get(self, num = 0, origin = False, update = False):
        """request the profit history data when necessary, cache the data and return it.

        :param num: num param only works when origin is False, can't be negative.
                    When num is 0, return the history data starting from the creation date of the portfolio,
                    when num is postive integer N, only return the history data starting from N num ago.
        :param origin: (optional, defaults to False) return the origin data from the api when origin is true, otherwise, return a simple customed version.
        :param update: (optional, defaults to False) try to reuse the cache if update is false, otherwise, request and update the cache.

        :rtype: list
        """
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
        if num > 0:
            return self._simple[-num:]
        return self._simple
