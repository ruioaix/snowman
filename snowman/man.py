"""
"""
from .session import Session
from .info import Info
from .profit import Profit
from .analysis import Analysis

class Snowman(object):

    def __init__(self):
        self.s = Session()
    
    def login(self, username, password):
        self.s.login(username, password)
    
    def get_info(self, symbol, origin = False):
        i = Info(symbol, self.s)
        return i.get(origin)

    def get_profit(self, symbol, days = 0, origin = False):
        p = Profit(symbol, self.s)
        return p.get(days = days, origin = origin)

    def get_analysis_benefit(self, symbol, origin = False):
        a = Analysis(symbol, self.s)
        return a.benefit(origin)

    def get_analysis_max_draw(self, symbol, origin = False):
        a = Analysis(symbol, self.s)
        return a.max_draw(origin)

    def get_analysis_turnover(self, symbol, origin = False):
        a = Analysis(symbol, self.s)
        return a.turnover(origin)

    def get_analysis_liquidity(self, symbol, origin = False):
        a = Analysis(symbol, self.s)
        return a.liquidity(origin)

    def get_analysis_volatility(self, symbol, origin = False):
        a = Analysis(symbol, self.s)
        return a.volatility(origin)

    def get_analysis_top_stocks(self, symbol, page = 1, count = 5, origin = False):
        a = Analysis(symbol, self.s)
        return a.top_stocks(page = page, count = count, origin = origin)

    def get_analysis(self, symbol):
        a = Analysis(symbol, self.s)
        return a.all()
