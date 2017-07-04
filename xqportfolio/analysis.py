"""
"""
import requests

from .headers import default_headers
from .urls import urls

class Analysis(object):

    def __init__(self, symbol):
        self.symbol = symbol
        self.s = requests.Session()
        self.s.headers = default_headers()
        self.islogin = False
        self.benefit_origin = None
        self.benefit_simple = None

    def _update_benefit(self):
        resp = s.get(urls.analysis_benefit(self.symbol))

    def _update_max_draw(self):
        pass

    def _update_turnover(self):
        pass

    def _update_liquidity(self):
        pass

    def _update_volatility(self):
        pass

    def _update_top_stocks(self):
        pass

    def _update(self):
        if not self.islogin:
            s.post()
        self._update_benefit()
        self._update_max_draw()
        self._update_liquidity()
        self._update_turnover()
        self._update_volatility()
        self._update_top_stocks()

    def benefit(self, origin = False, update = False):
        pass
