Snowman: Play Snowball
======================

.. image:: https://readthedocs.org/projects/snowman/badge/?version=latest
    :target: http://snowman.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Snowman is an interactive system for portfolios on xueqiu.com, including a library and a simple command line tool.

Simple example of Snowman tool:

.. code-block:: sh

    >>> snowman info ZH123456
    {'symbol': 'ZH123456', 'name': '绝代双骄', 'market': 'cn', 'status': 'active', 'created': '2015.01.07', 'updated_at': '2017-05-11 04:04:13', 'net_value': 1.3235, 'follower_count': 1}
    >>> snowman owner ZH123456
    {'id': 2246830809, 'screen_name': '小目学秀荣', 'description': '长期关注同仁堂，茅台。自认是价值投资的学习者。', 'followers_count': 19, 'friends_count': 179, 'status_count': 97}

Simple example of Snowman library:

.. code-block:: python

    >>> from snowman import Info
    >>> info = Info('ZH123456')
    >>> info.get()
    {'symbol': 'ZH123456', 'name': '绝代双骄', 'market': 'cn', 'status': 'active', 'created': '2015.01.07', 'updated_at': '2017-05-11 04:04:13', 'net_value': 1.3235, 'follower_count': 1}
    >>> info.owner()
    {'id': 2246830809, 'screen_name': '小目学秀荣', 'description': '长期关注同仁堂，茅台。自认是价值投资的学习者。', 'followers_count': 19, 'friends_count': 179, 'status_count': 97}
    >>>from snowman import Analysis
    >>>ana = Analysis('ZH123456')
    >>>ana.turnover()
    0.003
    >>>ana.topstocks()
    [{'symbol': 'SH601009', 'name': '南京银行', 'benefit': 0.17390683596197054, 'holding_duration': 911}, {'symbol': 'SZ000895', 'name': '双汇发展', 'benefit': 0.16364759739488366, 'holding_duration': 911}]

Snowman allows you to get most of the information of the portfolios on `xueqiu.com <https://xueqiu.com>`_ website.

Feature Support
---------------

Snowman supports Python 3.3-3.6.

Snowman supports following query functionalities:

- basic information, including name, owner, creation date, current holding and so on.
- analysis data, including turnover, liquidity and so on.
- profit history
- rebalancing history

Installation
____________

To install Snowman, simply

.. code-block:: bash
    
    $ pip install snowman

Documentation
-------------

Documentation is available at http://snowman.readthedocs.io

TODO
----

- portfolio-rebalancing functionality.
