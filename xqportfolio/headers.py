"""
"""

_default_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en,de;q=0.8,en-US;q=0.6,zh-TW;q=0.4,zh;q=0.2,zh-CN;q=0.2,af;q=0.2',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
}

def default_headers():
    return _default_headers.copy()
