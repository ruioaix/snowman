"""
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
        self.turnover_origin, self.turnover_simple = self._save(self.turnover_origin,
                                                                self.turnover_simple,
                                                                urls.analysis_turnover(self.symbol),
                                                                lambda origin_data: origin_data['values'][0]['value'],
                                                                origin = origin,
                                                                update = update)
        return self.turnover_origin if origin else self.turnover_simple

    def liquidity(self, origin = False, update = False):
        self.liquidity_origin, self.liquidity_simple = self._save(self.liquidity_origin,
                                                                  self.liquidity_simple,
                                                                  urls.analysis_liquidity(self.symbol),
                                                                  lambda origin_data: origin_data['values'][0]['value'],
                                                                  origin = origin,
                                                                  update = update)
        return self.liquidity_origin if origin else self.liquidity_simple

    def volatility(self, origin = False, update = False):
        self.volatility_origin, self.volatility_simple = self._save(self.volatility_origin,
                                                                    self.volatility_simple,
                                                                    urls.analysis_volatility(self.symbol),
                                                                    lambda origin_data: origin_data['volatility_rate'],
                                                                    origin = origin,
                                                                    update = update)
        return self.volatility_origin if origin else self.volatility_simple

    def top_stocks(self, page = 1, count = 5, origin = False, update = False):
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

    def all(self, origin):
        return {'benefit': self.benefit(origin = origin),
                'turnover': self.turnover(origin = origin),
                'liquidity': self.liquidity(origin = origin),
                'volatility': self.volatility(origin = origin),
                'max_draw': self.max_draw(origin = origin),
                'top_stocks': self.top_stocks(origin = origin),
                }
