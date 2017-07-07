"""

"""


__version__ = '0.0.1'

import logging
# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description = 'A interactive system for portfolios on xueqiu.com') 
    parser.add_argument('-v', '--version', action = 'version', version = '%(prog)s ' + __version__, 
                        help = 'print the snowman version and exit.')
    parser.add_argument('-D', '--debug', action = 'store_const', dest = 'verbosity', const = logging.DEBUG, default = logging.INFO,
                        help = 'show all messages, including debug messages.')

    parser.add_argument('action', help = 'return the basic information of the portfolio.')
    parser.add_argument('symbol', help = 'return the basic information of the portfolio.')

    parser.add_argument('-O', '--origin', action = 'store_true', 
                        help = 'return the origin content from xueqiu instead of the simple version.')

    parser.add_argument('-f', '--ofile', help = 'don\'t reuse the cache, fetch latest data from xueqiu.com.')

    return parser.parse_args()

from .man import Snowman
from .log import init
import json

def main():
    args = parse_arguments()
    init(args.verbosity)
    log = logging.getLogger(__name__)
    man = Snowman()
    try:
        get = getattr(man, 'get_' + args.action)
    except AttributeError:
        log.info('Snowman doesn\'t know what is "{}".'.format(args.action))
        return
    log.info('Snowman is on.') 
    res = get(args.symbol, origin = args.origin)
    if args.ofile:
        with open(args.ofile, 'w') as fo:
            json.dump(res, fo)
        log.info('Snowman saves the data into file "{}".'.format(args.ofile))
        return
    log.info('Snowman gets:')
    print(res)
