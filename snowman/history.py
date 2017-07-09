"""
snowman.History
~~~~~~~~~~~~~~~~

This module provides a history object to get rebalancing history data of the portfolios 
on xueqiu.com
"""
import json
import logging

from .urls import urls
from .session import Session
from .exceptions import WrongStatusCode, JsonLoadError, HistoryContentError

log = logging.getLogger(__name__)

class History(object):
    """ the rebalancing history information of a portfolio. 
    
    :param symbol: the portfolio symbol, a string starting with 'ZH'
    :param session: (optional) the session object responsible for http(s) connection 

    Usage::

    >>> from snowman import History
    >>> his = History('ZH123456')
    >>> his.get() #query all the rebalancing records of portfolio ZH123456.
    >>> his.get(10) #query the latest 10 records of portfolio ZH123456
    >>> his.get(10, 1, 3) 
    >>> # query the latest 10 records,  if there are no less than 12 records, 
    >>> # 4 requests will be sent,the count of result will be 12.
    >>> # otherwise, just return all the records.
    >>> his.get(origin = True) # return all the records in origin version.
    >>> his.get(page = 1, count = 3) #return all the records, query 3 records each time.

    """

    def __init__(self, symbol, session = None):
        self.symbol = symbol

        self.s = session if session else Session()

        #: the origin rebalancing data from xueqiu
        self._history = None

        #: the simple version data
        self._simple = None

    def be_login(self):
        """ make sure snowman has logined xueqiu.com. """
        self.s.be_login()

    def _req(self, page, count):
        """ request and return the origin data.  """
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
        """ merge data from multiple requests, and validate data integrity. 
        if data has flaws, a warning message will be emitted by logging.
        """
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

    def _update(self, num, page, count):
        """ send mutliple requests, until getting enough history or there are no more data. """
        data = {}
        while num == 0 or 'list' not in data or len(data['list']) < num:
            _data = self._req(page, count)
            if not _data or not _data['list']:
                break
            self._merge(data, _data)
            page += 1
        return data 

    def get(self, num = 0, page = 1, count = 20, origin = False, update = False):
        """request the history data when necessary, cache the data and return it.
        
        :param num: (optional, defaults to 0) this param specifies how many rebalance records
                            snowman needs to query at least. The actual count of the result depends on 
                            history, page and count. these three works together to decide the result.
                            when num is 0, all the records will be queried.
        :param page: (optional, defaults to 1) this param works with count param, each request will return
                    all the records in the range [(page - 1) * count + 1, page * count]. When num is
                    positive number N, snowman will send mutliple requests, each request return count records.
                    After the last request, the total number of records is (page * count), which will be not 
                    smaller than num or there are no more records.
        :param count: (optional, defaults to 20) check param page.
        :param origin: (optional, defaults to False) return the origin data from the api when origin is true, otherwise, return a simple customed version.
        :param update: (optional, defaults to False) try to reuse the cache if update is false, otherwise, request and update the cache.
        
        :rtype: dict
        """
        if update or self._history is None:
            self._history = self._update(num, page, count)
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
