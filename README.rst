krakenex
========

Kraken.com exchange API, Python 3 package.


Installation
-----------

This package requires Python 3.3 or later.

Run ``python3 ./setup.py install`` to install system-wide. Add ``--user``
to install locally for the user. The module will be called ``krakenex``.

A `PyPI package`_ is also available.

.. _PyPI package: https://pypi.python.org/pypi/krakenex


Documentation
-------------

The code is simple and documented in docstrings.

You can also view it online_, or generate your own with
``sphinx`` in ``doc``.

For a list of public/private API methods, see
`Kraken API documentation`_.

.. _online: https://veox.github.io/python3-krakenex
.. _Kraken API documentation: https://www.kraken.com/help/api


Development
-----------

This package will never support Python 2. There will be no changes made
to enable compatibility with Python 2. Python 3.0 was `released in
2008`_. It is more than 7 years old.

If you need to use Python 2, see python2-krakenex_.

.. _released in 2008: https://en.wikipedia.org/wiki/History_of_Python#Version_3.0


Attribution
-----------

Core code is licensed under LGPLv3. See ``LICENSE.txt``.

Examples are licensed under the Simplified BSD license. See
``examples/LICENSE.txt``.

`Payward's PHP API`_, Alan McIntyre's `BTC-e API`_,
and ScriptProdigy's `Cryptsy Python API`_ were used as
examples when writing the original python2-krakenex_ package.
It was then ported to Python 3.

.. _Payward's PHP API: https://github.com/payward/kraken-api-client
.. _BTC-e API: https://github.com/alanmcintyre/btce-api
.. _Cryptsy Python API: https://github.com/ScriptProdigy/CryptsyPythonAPI
.. _python2-krakenex: https://github.com/veox/python2-krakenex

