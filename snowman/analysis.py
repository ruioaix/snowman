"""
snowman.Analysis
~~~~~~~~~~~~~~~~

This module provides a analysis object to get all kinds of analysis data of the portfolios 
on xueqiu.com
"""
import re
import json
import logging

from .headers import default_headers
from .urls import urls
from .session import Session
from .exceptions import JsonLoadError, WrongStatusCode, AnalysisContentError

log = logging.getLogger(__name__)

class Analysis(object):
    """ the analysis information of a portfolio. 

    :param symbol: the portfolio symbol, a string starting with 'ZH'
    :param session: (optional) the session object responsible for http(s) connection 

    Usage::

    >>> from snowman import Analysis
    >>> ana = Analysis('ZH123456')
    >>> ana.benefit() # return benefit analysis data
    >>> ana.turnover() # return turnover analysis data
    >>> ...
    
    """

    def __init__(self, symbol, session = None):
        self.symbol = symbol
        self.s = session if session else Session()
        self.benefit_origin = None
        self.benefit_simple = None
        self.max_draw_origin = None
        self.max_draw_simple = None
        self.turnover_origin = None
        self.turnover_simple = None
        self.liquidity_origin = None
        self.liquidity_simple = None
        self.volatility_origin = None
        self.volatility_simple = None
        self.top_stocks_origin = None
        self.top_stocks_simple = None

    def _update(self, url):
        """ to get raw data """
        self.s.touch()
        log.debug('request ' + url)
        resp = self.s.get(url)
        if resp.status_code != 200:
            raise WrongStatusCode(resp.status_code)
        try:
            data = json.loads(resp.text)
        except json.decoder.JSONDecodeError:
            raise JsonLoadError('"{}..."'.format(resp.text[:50]))
        return data

    def _save(self, origin_data, simple_data, url, origin_to_simple, origin = False, update = False):
        """ an abstruct function contain the logic of cache """
        if update or origin_data is None:
            origin_data = self._update(url)
            simple_data = None
        if origin : return origin_data, simple_data
        if simple_data is None:
            if origin_data == {'success': False} or origin_data == []:
                simple_data = origin_data
            else:
                try:
                    simple_data = origin_to_simple(origin_data)
                except KeyError as e:
                    raise AnalysisContentError(str(e))
        return origin_data, simple_data
    
    def benefit(self, origin = False, update = False):
        """ benefit analysis data 
        
        :param origin: (optional, defaults to False) return the origin data from the api when origin is true, otherwise, return a simple customed version.
        :param update: (optional, defaults to False) try to reuse the cache if update is false, otherwise, request and update the cache.

        :rtype: list
        """
        origin_to_simple = lambda origin_data: [(int(re.sub('-', '', month['date'])), month['value']) 
                                           for month in origin_data[0]['profit_list']]
        self.benefit_origin, self.benefit_simple = self._save(self.benefit_origin, 
                                         self.benefit_simple,
                                         urls.analysis_benefit(self.symbol),
                                         origin_to_simple,
                                         origin = origin,
                                         update = update)
        return self.benefit_origin if origin else self.benefit_simple

    def max_draw(self, origin = False, update = False):
        """ max draw analysis data 
        
        :param origin: (optional, defaults to False) return the origin data from the api when origin is true, otherwise, return a simple customed version.
        :param update: (optional, defaults to False) try to reuse the cache if update is false, otherwise, request and update the cache.

        :rtype: dict
        """
        def origin_to_simple(origin_data):
            simple_data = {}
            simple_data['begin_date'] = origin_data['begin_date']
            simple_data['end_date'] = origin_data['end_date']
            simple_data['value'] = origin_data['max_draw']
            return simple_data
        self.max_draw_origin, self.max_draw_simple = self._save(self.max_draw_origin,
                                                                self.max_draw_simple,
                                                                urls.analysis_max_draw(self.symbol),
                                                                origin_to_simple,
                                                                origin = origin,
                                                                update = update)
        return self.max_draw_origin if origin else self.max_draw_simple

    def turnover(self, origin = False, update = False):
        """ turnover analysis data 
        
        :param origin: (optional, defaults to False) return the origin data from the api when origin is true, otherwise, return a simple customed version.
        :param update: (optional, defaults to False) try to reuse the cache if update is false, otherwise, request and update the cache.

        :rtype: dict if origin is True, otherwise an float number
        """
        self.turnover_origin, self.turnover_simple = self._save(self.turnover_origin,
                                                                self.turnover_simple,
                                                                urls.analysis_turnover(self.symbol),
                                                                lambda origin_data: origin_data['values'][0]['value'],
                                                                origin = origin,
                                                                update = update)
        return self.turnover_origin if origin else self.turnover_simple

    def liquidity(self, origin = False, update = False):
        """ liquidity analysis data 
        
        :param origin: (optional, defaults to False) return the origin data from the api when origin is true, otherwise, return a simple customed version.
        :param update: (optional, defaults to False) try to reuse the cache if update is false, otherwise, request and update the cache.

        :rtype: dict if origin is True, otherwise an float number
        """
        self.liquidity_origin, self.liquidity_simple = self._save(self.liquidity_origin,
                                                                  self.liquidity_simple,
                                                                  urls.analysis_liquidity(self.symbol),
                                                                  lambda origin_data: origin_data['values'][0]['value'],
                                                                  origin = origin,
                                                                  update = update)
        return self.liquidity_origin if origin else self.liquidity_simple

    def volatility(self, origin = False, update = False):
        """ volatility analysis data 
        
        :param origin: (optional, defaults to False) return the origin data from the api when origin is true, otherwise, return a simple customed version.
        :param update: (optional, defaults to False) try to reuse the cache if update is false, otherwise, request and update the cache.

        :rtype: dict if origin is True, otherwise an float number
        """
        self.volatility_origin, self.volatility_simple = self._save(self.volatility_origin,
                                                                    self.volatility_simple,
                                                                    urls.analysis_volatility(self.symbol),
                                                                    lambda origin_data: origin_data['volatility_rate'],
                                                                    origin = origin,
                                                                    update = update)
        return self.volatility_origin if origin else self.volatility_simple

    def top_stocks(self, page = 1, count = 5, origin = False, update = False):
        """ volatility analysis data 
        
        :param page: (optional, defaults to 1) this param works with count param.
                    if page is N, the result is stocks ranking between [(N - 1) * count + 1, N * count]
                    so when page is 1, the result is top [count] stocks.
        :param count: (optional, defaults to 5) check page param.
        :param origin: (optional, defaults to False) return the origin data from the api when origin is true, otherwise, return a simple customed version.
        :param update: (optional, defaults to False) try to reuse the cache if update is false, otherwise, request and update the cache.

        :rtype: dict if origin is True, otherwise list
        """
        origin_to_simple = lambda origin_data: [{'symbol': st['stock_symbol'], 
                                                 'name': st['stock_name'], 
                                                 'benefit': st['stock_benefit'], 
                                                 'holding_duration': st['holding_duration']} 
                                                for st in origin_data['stock_list']]
        self.top_stocks_origin, self.top_stocks_simple = self._save(self.top_stocks_origin,
                                                                    self.top_stocks_simple,
                                                                    urls.analysis_top_stocks(self.symbol, page = page, count = count),
                                                                    origin_to_simple,
                                                                    origin = origin,
                                                                    update = update)
        return self.top_stocks_origin if origin else self.top_stocks_simple 

    def all(self, page = 1, count = 5, origin = False):
        """ update all the caches, and return all analysis data in a single dict.

        :param page: (optional, defaults to 1) this only affect the data for top stocks.
                    this param works with count param.
                    if page is N, the result is stocks ranking between [(N - 1) * count + 1, N * count]
                    so when page is 1, the result is top [count] stocks.
        :param count: (optional, defaults to 5) this only affect the data for top stocks. Check page param.
        :param origin: (optional, defaults to False) return the origin data from the api when origin is true, otherwise, return a simple customed version.
        :param update: (optional, defaults to False) try to reuse the cache if update is false, otherwise, request and update the cache.

        :rtype: dict
        """
        return {'benefit': self.benefit(origin = origin),
                'turnover': self.turnover(origin = origin),
                'liquidity': self.liquidity(origin = origin),
                'volatility': self.volatility(origin = origin),
                'max_draw': self.max_draw(origin = origin),
                'top_stocks': self.top_stocks(page = page, count = count, origin = origin),
                }
