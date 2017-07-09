"""
snowman.Info
~~~~~~~~~~~~

This module provides a Info object to get basic information of the portfolios 
on xueqiu.com
"""
import re
import json
import logging
import datetime

from .urls import urls
from .session import Session
from .exceptions import WrongStatusCode, InfoContentError, JsonLoadError

log = logging.getLogger(__name__)

class Info(object):
    """ the basic information of a portfolio. 
    
    :param symbol: the portfolio symbol, a string starting with 'ZH'
    :param session: (optional) the session object responsible for http(s) connection 

    Usage::

    >>> from snowman import Info
    >>> info = Info('ZH123456')
    >>> info.get()
    >>> info.owner()
    >>> info.holdings()

    """

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
        """ to get raw data """
        url = urls.info(self.symbol)
        log.debug("request " + url)
        resp = self.s.get(url)
        if resp.status_code != 200:
            raise WrongStatusCode("Info gets {} http status code.".format(resp.status_code))
        cubeinfo = re.search(r'(?<=SNB.cubeInfo = ).*(?=;[\s]SNB.cubePieData)', resp.text)
        if cubeinfo is None: 
            raise InfoContentError("Info can not be found from url: '{}'".format(urls.info(self.symbol)))
        try:
            text = cubeinfo.group()
            data = json.loads(text)
        except json.decoder.JSONDecodeError:
            raise JsonLoadError('"{}..."'.format(text[:50]))
        return data

    def get(self, origin = False, update = False):
        """ request the data when necessary, cache the result and return it.

        :param origin: (optional, defaults to False) return the origin data from the api when origin is true, otherwise, return a simple customed version.
        :param update: (optional, defaults to False) try to reuse the cache if update is false, otherwise, request and update the cache.

        :rtype: dict
        """
        if update or self._info is None: 
            self._info = self._update()
            self._simple = None
        if origin: 
            return self._info
        if self._simple is None:
            try:
                self._simple = {'symbol': self.symbol}
                self._simple['name'] = self._info['name']
                self._simple['market'] = self._info['market']
                self._simple['status'] = 'active' if self._info['active_flag'] else 'closed'
                self._simple['created'] = self._info['created_date']
                updated_at = datetime.datetime.fromtimestamp(self._info['updated_at'] // 1000)
                self._simple['updated_at'] = updated_at.strftime('%Y-%m-%d %H:%M:%S')
                self._simple['net_value'] = self._info['net_value']
                self._simple['follower_count'] = self._info['follower_count']
            except KeyError as e:
                raise InfoContentError(str(e))
        return self._simple

    def owner(self, origin = False):
        """ return the owner information which is contained as a part of the basic information. 

        :param origin: (optional, defaults to False) return the origin data from the api when origin is true, otherwise, return a simple customed version.

        :rtype: dict
        
        """
        if self._info is None:
            self._info = self._update()
        try: 
            if origin:
                owner = self._info['owner']
            else:
                owner = {
                    'id': self._info['owner']['id'],
                    'screen_name': self._info['owner']['screen_name'],
                    'description': self._info['owner']['description'],
                    'followers_count': self._info['owner']['followers_count'],
                    'friends_count': self._info['owner']['friends_count'],
                    'status_count': self._info['owner']['status_count'],
                }
        except KeyError as e:
            raise InfoContentError("'owner' -> " + str(e))
        return owner

    def holdings(self, origin = False):
        """ return the current holdings of the portfolio, which is contained as a part of the basic information.
        
        :param origin: (optional, defaults to False) return the origin data from the api when origin is true, otherwise, return a simple customed version.
        
        :rtype: dict
        """
        if self._info is None:
            self._info = self._update()
        try:
            if origin:
                holdings = self._info['view_rebalancing']['holdings']
            else:
                holdings = [{
                    'symbol': stk['stock_symbol'], 
                    'name': stk['stock_name'], 
                    'volume': stk['volume'], 
                    'weight': stk['weight']} 
                        for stk in self._info['view_rebalancing']['holdings']]
        except KeyError as e:
            raise InfoContentError(str(e))
        return holdings
