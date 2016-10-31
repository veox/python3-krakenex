krakenex
========

Kraken.com exchange API, Python 3 package.


Installation
-----------

This package requires Python 3.3 or later.

Run `python3 ./setup.py install` to install system-wide. Add `--user`
to install locally for the user. The module will be called `krakenex`.

A [PyPI package][pypi] is also available.


Documentation
-------------

The code is simple and documented in docstrings.

You can also view it [online][githubpages], or generate your own with
`sphinx` in [doc](doc).

For a list of public/private API methods, see
[Kraken API documentation][krakenapidoc].


Attribution
-----------

Core code is licensed under the LGPLv3 license. It should be available in
`LICENSE`. If not, see [here][corelicense].

Examples are licensed under the Simplified BSD license. See
`examples/LICENSE`.

Payward's [PHP API][krakenphpapi], Alan McIntyre's [BTC-e API][btceapi],
and ScriptProdigy's [Cryptsy Python API][cryptsypyapi] were used as
examples when writing the original [Python 2 package][python2-krakenex].
It was then ported to Python 3.


[pypi]: https://pypi.python.org/pypi/krakenex
[krakenapidoc]: https://www.kraken.com/help/api
[corelicense]: https://www.gnu.org/licenses/lgpl-3.0.txt
[krakenphpapi]: https://github.com/payward/kraken-api-client
[btceapi]: https://github.com/alanmcintyre/btce-api
[cryptsypyapi]: https://github.com/ScriptProdigy/CryptsyPythonAPI
[python2-krakenex]: https://github.com/veox/python2-krakenex
[githubpages]: https://veox.github.io/python3-krakenex
