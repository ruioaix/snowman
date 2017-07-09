Tool: snowman
=============

usage::

>>> snowman verb object [-h] [-v] [-D] [-O] [-f OFILE] [-P PARAMS [PARAMS ...]]
               
positional arguments:
  verb                  specify the action snowman need to perform.
  object                the object related to the action.

available verb:

.. code-block:: sh

    $ snowman info ZHXXXXXX
    $ snowman owner ZHXXXXXX
    $ snowman holdings ZHXXXXXX
    $ snowman profit ZHXXXXXX
    $ snowman benefit ZHXXXXXX
    $ snowman maxdraw ZHXXXXXX
    $ snowman turnover ZHXXXXXX
    $ snowman liquidity ZHXXXXXX
    $ snowman volatility ZHXXXXXX
    $ snowman topstocks ZHXXXXXX
    $ snowman analysis ZHXXXXXX
    $ snowman history ZHXXXXXX

optional arguments:

  -h, --help            show this help message and exit
  -v, --version         print the snowman version and exit.
  -D, --debug           show all messages, including debug messages.
  -O, --origin          return the origin content from xueqiu instead of the simple version.
  -f OFILE              save the result data into specified file.
  -P params-list        parameters for actions.

Example:

.. code-block:: sh

    $ snowman info ZH123456 #return the basic information of portfolio ZH123456 in simple format.
    {'symbol': 'ZH123456', 'name': '绝代双骄', 'market': 'cn', 'status': 'active', 'created': '2015.01.07', 'updated_at': '2017-05-11 04:04:13', 'net_value': 1.3235, 'follower_count': 1}
    $ snowman info ZH123456 -O # return the basic information of portfolio ZH123456 in origin format. 
    $ snowman profit ZH123456 -P 33 # return the latest 33 days profit data of portfolio ZH123456 in simple format.
    $ snowman topstocks ZH123456 -P 20 # return the top 20 best-profit stocks of porfolio ZH123456
    $ snowman history ZH123456 -P 30 2 10 # return 30 rebalancing records starting from 10.
