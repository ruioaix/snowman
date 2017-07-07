"""
"""
from .session import Session
from .info import Info
from .profit import Profit
from .analysis import Analysis
from .history import History

class Snowman(object):

    def __init__(self):
        self.s = Session()
    
    def login(self, username, password):
        self.s.login(username, password)
    
    def info(self, symbol, origin = False):
        i = Info(symbol, self.s)
        return i.get(origin)

    def owner(self, symbol, origin = False):
        i = Info(symbol, self.s)
        return i.owner(origin)

    def holdings(self, symbol, origin = False):
        i = Info(symbol, self.s)
        return i.holdings(origin)

    def profit(self, symbol, days = 0, origin = False):
        p = Profit(symbol, self.s)
        return p.get(days = days, origin = origin)

    def benefit(self, symbol, origin = False):
        a = Analysis(symbol, self.s)
        return a.benefit(origin)

    def maxdraw(self, symbol, origin = False):
        a = Analysis(symbol, self.s)
        return a.max_draw(origin)

    def turnover(self, symbol, origin = False):
        a = Analysis(symbol, self.s)
        return a.turnover(origin)

    def liquidity(self, symbol, origin = False):
        a = Analysis(symbol, self.s)
        return a.liquidity(origin)

    def volatility(self, symbol, origin = False):
        a = Analysis(symbol, self.s)
        return a.volatility(origin)

    def topstocks(self, symbol, page = 1, count = 5, origin = False):
        a = Analysis(symbol, self.s)
        return a.top_stocks(page = page, count = count, origin = origin)

    def analysis(self, symbol, origin = False):
        a = Analysis(symbol, self.s)
        return a.all(origin)

    def history(self, symbol, history_num = 0, origin = False):
        h = History(symbol, self.s)
        return h.get(history_num, origin)
