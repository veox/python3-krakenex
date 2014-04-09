krakenex
========

**NOTE**: work in progress to port krakenex from Python 2 to 3.

Kraken.com exchange API, Python 3 package.


Installation
-----------

Run `python ./setup.py install`. The module will be called `krakenex`.


Documentation
-------------

The code is simple and documented in docstrings.

For a list of public/private API methods, see
[Kraken API documentation][krakenapidoc].


Attribution
-----------

This code is licensed under the GPLv3 license. It should be available in
`LICENSE`. If not, see [here][gnugpl].

Payward's [PHP API][krakenphpapi], Alan McIntyre's [BTC-e API][btceapi],
and ScriptProdigy's [Cryptsy Python API][cryptsypyapi] were used as
examples.


[gnugpl]: https://www.gnu.org/licenses/gpl-3.0.txt
[krakenphpapi]: https://github.com/payward/kraken-api-client
[btceapi]: https://github.com/alanmcintyre/btce-api
[cryptsypyapi]: https://github.com/ScriptProdigy/CryptsyPythonAPI
[krakenapidoc]: https://www.kraken.com/help/api
