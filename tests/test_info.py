import pytest
from snowman import Info
from snowman import exceptions


def test_info_not_exist_attribute():
    symbol = 'ZH123456'
    info = Info(symbol).get(origin = True)
    with pytest.raises(AttributeError):
        info.nonexist

def test_info_not_exist_portfolio():
    symbol = 'ZH1'
    with pytest.raises(exceptions.WrongStatusCode):
        Info(symbol).get()
