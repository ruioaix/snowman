"""
"""
import json
import logging

from .urls import urls
from .session import Session
from .exceptions import WrongStatusCode, JsonLoadError, HistoryContentError

log = logging.getLogger(__name__)

class History(object):

    def __init__(self, symbol, session = None):
        self.symbol = symbol
        self.s = session if session else Session()
        self._history = None
        self._simple = None

    def be_login(self):
        self.s.be_login()

    def _req(self, page, count):
        self.be_login()
        url = urls.history(self.symbol, page, count)
        log.debug('requst ' + url)
        resp = self.s.get(url)
        if resp.status_code == 400:
            log.debug('History query exceed limitation.')
            return {}
        if resp.status_code != 200:
            raise WrongStatusCode(resp.status_code)
        try:
            data = json.loads(resp.text)
        except json.decoder.JSONDecoderError:
            raise JsonLoadError('"{}..."'.format(resp.text[:50]))
        return data

    def _merge(self, data, _data):
        try:
            validate = {}
            if not data:
                data['max_page'] = _data['maxPage']
                data['total_count'] = _data['totalCount']
                data['list'] = [_data['list'][0]]
            for act in _data['list']:
                if act['id'] < data['list'][-1]['id']:
                    if act['status'] == 'success':
                        for reb in act['rebalancing_histories']:
                            symbol = reb['stock_symbol']
                            if symbol in validate and validate[symbol][1] != reb['volume']:
                                    log.warning('the history data of {} has flaws; {}:{}->{}'.format(
                                        self.symbol, symbol, validate[symbol], (act['id'], reb['volume'])))
                            validate[symbol] = (act['id'], reb['prev_volume'] if reb['prev_volume'] else 0)
                    data['list'].append(act)
            data['count'] = len(data['list'])
        except KeyError as e:
            raise HistoryContentError(str(e))

    def _update(self, history_num, page, count):
        data = {}
        while history_num == 0 or 'list' not in data or len(data['list']) < history_num:
            _data = self._req(page, count)
            if not _data or not _data['list']:
                break
            self._merge(data, _data)
            page += 1
        return data 

    def get(self, history_num = 0, page = 1, count = 20, origin = False, update = False):
        if update or self._history is None:
            self._history = self._update(history_num, page, count)
            self._simple = None
        if origin:
            return self._history
        if self._simple is None:
            try:
                self._simple = {
                    'max_page': self._history['max_page'],
                    'total_count': self._history['total_count'],
                    'count': self._history['count'],
                }
                self._simple['list'] = []
                for act in self._history['list']:
                    if act['status'] != 'success': continue
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
            except KeyError as e:
                raise HistoryContentError(str(e))
        return self._simple
