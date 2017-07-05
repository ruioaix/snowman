"""
"""

class Urls(object):

    _urls = {
        'base': 'https://xueqiu.com',
        'login': 'https://xueqiu.com/user/login',
        'info': 'https://xueqiu.com/P/{}',
        'profit': 'https://xueqiu.com/cubes/nav_daily/all.json?cube_symbol={}',
        'analysis_benefit': 'https://xueqiu.com/cubes/analyst/histo/benefit.json?cube_symbol={}',
        'analysis_max_draw': 'https://xueqiu.com/cubes/analyst/histo/stat.json?cube_symbol={}&type=max_draw',
        'analysis_liquidity': 'https://xueqiu.com/cubes/analyst/histo/stat.json?cube_symbol={}&type=liquidity',
        'analysis_turnover': 'https://xueqiu.com/cubes/analyst/histo/stat.json?cube_symbol={}&type=turnover',
        'analysis_volatility': 'https://xueqiu.com/cubes/analyst/histo/stat.json?cube_symbol={}&type=volatility',
        'analysis_top_stocks': 'https://xueqiu.com/cubes/analyst/stock.json?cube_symbol={}&page={}&count={}&type=gain',
        'history': 'https://xueqiu.com/cubes/rebalancing/history.json?cube_symbol={}&count={}&page={}',
    }

    def __getattr__(self, name):
        if name in self._urls:
            return self._urls[name]
        raise AttributeError("'{}' object has no attribut '{}'".format(Urls.__name__, name))

    def info(self, symbol):
        return self._urls['info'].format(symbol)

    def profit(self, symbol):
        return self._urls['profit'].format(symbol)

    def analysis_benefit(self, symbol):
        return self._urls['analysis_benefit'].format(symbol)

    def analysis_max_draw(self, symbol):
        return self._urls['analysis_max_draw'].format(symbol)

    def analysis_liquidity(self, symbol):
        return self._urls['analysis_liquidity'].format(symbol)

    def analysis_turnover(self, symbol):
        return self._urls['analysis_turnover'].format(symbol)

    def analysis_volatility(self, symbol):
        return self._urls['analysis_volatility'].format(symbol)

    def analysis_top_stocks(self, symbol, page = 1, count = 5):
        return self._urls['analysis_top_stocks'].format(symbol, page, count)

    def history(self, symbol, page = 1, count = 20):
        return self._urls['history'].format(symbol, count, page)

urls = Urls()
