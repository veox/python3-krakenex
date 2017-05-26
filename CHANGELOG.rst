python3-krakenex change log
===========================

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_, and this project adheres
to `semantic versioning`_.

.. _Keep a Changelog: http://keepachangelog.com/
.. _semantic versioning: http://semver.org/

[vX.Y.Z] - Unreleased (Anyday)
------------------------------

Added
^^^^^
* More examples.

Changed
^^^^^^^
* Renamed ``NEWS`` to ``CHANGELOG``.

[v0.1.5a] - Unreleased (Anyday)
------------------------------

Added
^^^^^
* Updated kraken connection to raise error in case it doesnt receive 20x status code. 


[v0.1.4] - 2017-03-27 (Monday)
------------------------------
  
Changed
^^^^^^^
* Properly release key file descriptor after reading in key.
* Verbose docs, served at ``https://python3-krakenex.readthedocs.io/``.

[v0.1.3] - 2017-01-31 (Tuesday)
-------------------------------
  
Changed
^^^^^^^
* Single-source version and URL - used during setup and in ``User-Agent``.

[v0.1.2] - 2016-11-05 (Saturday)
--------------------------------

Changed
^^^^^^^
* Ship examples with PyPI package.

[v0.1.1] - 2016-11-05 (Saturday)
--------------------------------

Changed
^^^^^^^
* Renamed README and LICENSE according to PyPI recommendations.

[v0.1.0] - 2016-10-31 (Monday)
------------------------------

Added
^^^^^
* Now available on `PyPI`_ as a source distribution.

.. _PyPI: https://pypi.python.org/pypi/krakenex

Changed
^^^^^^^
* Change versioning scheme to semantic versioning (recommended by PyPI).

[v0.0.6.2] - 2016-04-18 (Monday)
--------------------------------

Added
^^^^^
* Basic documentation with sphinx.

[v0.0.6.1] - 2016-03-25 (Friday)
--------------------------------

Changed
^^^^^^^
* Classes sub-classed from ``object``.

[v0.0.6] - 2014-07-22 (Tuesday)
-------------------------------

Changed
^^^^^^^
* Core license changed from GPLv3 to LGPLv3. Examples remain at Simplified BSD.

[v0.0.5] - 2014-05-01 (Thursday)
--------------------------------

Added
^^^^^
* ``API.set_connection()`` method to set default connection.

[v0.0.4.1] - 2014-04-30 (Wednesday)
-----------------------------------

Changed
^^^^^^^
* Fixed ``User-Agent`` still reporting version ``0.0.3``.

[v0.0.4] - 2014-04-11 (Friday)
------------------------------

Added
^^^^^
* ``conditional-close`` example.
* Examples licensed under the Simplified BSD license.

Changed
^^^^^^^
* Original Python 2 version ported to Python 3.

[v0.0.3] - 2014-01-10 (Friday)
------------------------------

Added
^^^^^
* ``API.load_key()`` method to allow loading key/secret pair from file.

[v0.0.2] - 2014-01-04 (Saturday)
--------------------------------

Added
^^^^^
* Basic implementation of ``KrakenConnection`` class.
* Optional ``conn`` argument to query methods allows connection reuse.

[v0.0.1] - 2013-12-13 (Wednesday)
---------------------------------

Added
^^^^^
* Basic ``API`` class with ``query_{public,private}()`` methods.
* Licensed under GPLv3.
