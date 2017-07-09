"""

"""


__version__ = '0.1.0'

from .info import Info
from .profit import Profit
from .analysis import Analysis
from .history import History

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

    parser.add_argument('verb', help = 'specify the action snowman need to perform.')
    parser.add_argument('object', help = 'the object related to the action.')

    parser.add_argument('-O', '--origin', action = 'store_true', 
                        help = 'return the origin content from xueqiu instead of the simple version.')

    parser.add_argument('-f', '--ofile', help = 'save the result data into specified file.')

    parser.add_argument('-P', '--params', nargs = '+', help = 'parameters for actions.')

    return parser.parse_args()

from .man import Snowman
from .log import init
import json

def main():
    """ main of snowman """
    args = parse_arguments()
    init(args.verbosity)
    log = logging.getLogger(__name__)
    man = Snowman()
    try:
        verb = getattr(man, args.verb)
    except AttributeError:
        log.info('Snowman doesn\'t know how to "{}".'.format(args.verb))
        return
    log.info('Snowman is on.') 
    if verb == man.profit:
        days = 0
        if args.params and args.params[0].isdigit():
            days = int(args.params[0])
        res = verb(args.object, days = days, origin = args.origin)
    elif verb == man.topstocks:
        page = 1
        count = 5
        if args.params and args.params[0].isdigit():
            if len(args.params) == 1:
                count = int(args.params[0])
            elif args.params[1].isdigit():
                page = int(args.params[0])
                count = int(args.params[1])
        res = verb(args.object, page = page, count = count, origin = args.origin)
    elif verb == man.history:
        history_num = 0
        page = 1
        count = 20
        if args.params and args.params[0].isdigit():
            if len(args.params) == 1:
                history_num = int(args.params[0])
            elif args.params[1].isdigit():
                if len(args.params) == 2:
                    page = int(args.params[0])
                    count = int(args.params[1])
                    history_num = -1
                elif args.params[2].isdigit():
                    history_num = int(args.params[0])
                    page = int(args.params[1])
                    count = int(args.params[2])
        res = verb(args.object, history_num = history_num, 
                   page = page, count = count, origin = args.origin)
    else:
        res = verb(args.object, origin = args.origin)
    if args.ofile:
        with open(args.ofile, 'w') as fo:
            json.dump(res, fo)
        log.info('Snowman saves the data into file "{}".'.format(args.ofile))
        return
    log.info('Snowman gets:')
    print(res)
