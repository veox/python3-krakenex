`krakenex`
==========

.. image:: https://badges.gitter.im/python3-krakenex/Lobby.svg
   :alt: Join the chat at https://gitter.im/python3-krakenex/Lobby
   :target: https://gitter.im/python3-krakenex/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

Kraken.com exchange API, Python 3 package.

This package is intentionally as lean as possible, and only
provides a minimal interface to the `Kraken`_ cryptocurrency
exchange.

Intended for developers, not traders.

.. _Kraken: https://kraken.com/


Software that uses `krakenex`
-----------------------------

* clikraken_ - command-line client for the Kraken exchange

.. _clikraken: https://github.com/zertrin/clikraken


Installation
------------

This package requires Python 3.3 or later. The module will be called
``krakenex``.

To install system-wide using standard-library ``setuptools``, run:

``python3 ./setup.py install``

Add ``--user`` to install locally for the user:

``python3 ./setup.py install --user``

A `PyPI package`_ is also available. To install system-wide using ``pip``:

``pip install krakenex``

Or, to install locally for the user:

``pip install --user krakenex``

.. _PyPI package: https://pypi.python.org/pypi/krakenex


Documentation
-------------

View the latest_ or stable_ online at ReadTheDocs.

The code is documented in docstrings, and can be viewed with a text editor.

You can also generate your own with, e.g., ``make html`` in ``doc``.
This requires ``sphinx`` and its ``rtd`` theme.

For a list of public/private Kraken API methods, see
their `API documentation`_.

.. _latest: https://python3-krakenex.readthedocs.io/en/latest/
.. _stable: https://python3-krakenex.readthedocs.io/en/stable/
.. _API documentation: https://www.kraken.com/help/api


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

