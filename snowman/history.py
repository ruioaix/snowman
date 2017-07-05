"""
"""
import json

from .urls import urls
from .session import Session

class History(object):

    def __init__(self, symbol, session = None):
        self.symbol = symbol
        self.s = session if session else Session()
        self._history = None
        self._simple = None

    def login(self, username, password):
        if not self.s.is_login():
            self.s.login(username, password)

    def _merge(self, data, _data):
        if not data:
            data['max_page'] = _data['maxPage']
            data['total_count'] = _data['totalCount']
            data['list'] = []
            data['list'].extend(_data['list'])
            return
        for act in _data['list']:
            if act['id'] < data['list'][-1]['id']:
                data['list'].append(act)

    def _update(self, history_num = 0):
        page = 1
        data = {}
        while history_num == 0 or not data or len(data['list']) < history_num:
            resp = self.s.get(urls.history(self.symbol, page))
            if resp.status_code == 400: break
            try:
                _data = json.loads(resp.text)
            except json.decoder.JSONDecodeError:
                raise Exception('Json loads error: {}'.format(resp.text[:50]))
            self._merge(data, _data)
            page += 1
        data['count'] = len(data['list'])
        return data 

    def get(self, history_num = 0, origin = False, update = False):
        if update or self._history is None:
            self._history = self._update(history_num)
            self._simple = None
        if origin:
            return self._history
        if self._simple is None:
            self._simple = {
                'max_page': self._history['max_page'],
                'total_count': self._history['total_count'],
                'count': self._history['count'],
            }
            self._simple['list'] = []
            for act in self._history['list']:
                if act['status'] == 'failed': continue
                _act = {
                    'id': act['id'],
                    'category': act['category'],
                    'created_at': act['created_at'],
                    'updated_at': act['updated_at'],
                    'stocks': []
                }
                self._simple['list'].append(_act)
                for stk in act['rebalancing_histories']:
                    _stk = {
                        'stock_symbol': stk['stock_symbol'],
                        'stock_name': stk['stock_name'],
                        'prev_volume': stk['prev_volume'],
                        'prev_weight': stk['prev_weight'],
                        'target_volume': stk['target_volume'],
                        'target_weight': stk['target_weight'],
                        'volume': stk['volume'],
                        'weight': stk['weight'],
                        'price': stk['price'],
                    }
                    _act['stocks'].append(_stk)
        return self._simple
