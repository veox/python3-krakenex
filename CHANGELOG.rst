python3-krakenex change log
===========================

All notable changes should be documented in this file.

The format is based on `Keep a Changelog`_, and this project adheres
to `semantic versioning`_.

.. _Keep a Changelog: http://keepachangelog.com/
.. _semantic versioning: http://semver.org/

[v2.0.0] - 2017-11-14 (Tuesday)
-------------------------------

For a detailed list of changes, refer to the same-number releases below.

Migration instructions
^^^^^^^^^^^^^^^^^^^^^^
* Everything network-related now handled by ``requests``. See its
  `docs`_ if needed. (`#11`_)
* ``krakenex.API`` class no longer has a ``conn`` attribute for
  connection manipulation. It has been replaced by a ``session``
  attribute, which is a ``requests.Session``. For custom networking
  setups, directly modify ``session`` attribute of a ``krakenex.API``
  object.
* ``krakenex.API`` constructor no longer accepts ``conn`` argument
  as a means of re-using an existing ``krakenex.Connection`` object.
  Instead, modify ``krakenex.API.session`` if needed, same as above.

.. _docs: http://docs.python-requests.org/
.. _#11: https://github.com/veox/python3-krakenex/issues/11

Known issues
^^^^^^^^^^^^
* The remote servers are unstable under high load, which is most of
  the time. No recovery mechanism is provided for failed queries. (`#66`_)

Most importantly, queries that may seem to have failed due to a ``502``
HTTP error may in fact reach the trade execution engine, with an
unpredictable delay. See `PSA`_ for an example.

After encountering a ``502``, a subsequent call to
``krakenex.API.query_private()`` will construct a new query, with an
increased ``nonce``. When used with an ``AddOrder`` query, this may
have disastrous effects, placing a duplicate order.

To work around this, instead reuse the ``krakenex.API.response.request``
object, which is a ``requests.PreparedRequest``, saved as part of
``requests``' operation when submitting the first query. This request
can be re-sent using ``krakenex.API.session.send()``.

.. _#66: https://github.com/veox/python3-krakenex/issues/66
.. _PSA: https://www.reddit.com/r/krakenex/comments/778uvh/psa_http_error_502_does_not_mean_the_query_wont/

[v2.0.0c2] - 2017-10-20 (Friday)
--------------------------------

**Release candidate.** Not recommended for production use.

Changed
^^^^^^^
* Fixed bug with dependencies not getting installed when following
  installation instructions in a clean virtual environment.

[v2.0.0c1] - 2017-10-20 (Friday)
--------------------------------

**Yanked** due to clean-room ``pip`` installation failing.

[v2.0.0a1] - 2017-09-21 (Thursday)
----------------------------------

**Internal alpha testing release!** Not for general use. For that
reason, ``pip`` package not provided.

Added
^^^^^
* ``krakenex.API.session`` attribute, which is a ``requests.Session``.
* ``krakenex.API.response`` attribute, which is a ``requests.Response``
  object for the previous query. It is available whether the query
  was successful or has failed.

Changed
^^^^^^^
* It is now recommended to install with ``pip`` in a ``virtualenv``.
  See ``README`` for details.

Removed
^^^^^^^
* ``krakenex.Connection`` class. Obsoleted by use of ``requests.Session``.
* ``krakenex.API.conn`` attribute, which was a ``krakenex.Connection``
  object.
* ``krakenex.API.set_connection()`` method (deprecated since ``v1.0.0``).

[v1.0.0] - 2017-09-18 (Monday)
------------------------------

For a detailed list of changes, refer to the same-number releases below.

Migration instructions
^^^^^^^^^^^^^^^^^^^^^^
* If you were previously calling ``API.query_private()`` or
  ``API.query_public()`` in a ``try/except`` block, be aware that
  these two may now throw a ``http.client.HTTPException``, if the
  underlying ``Connection`` returns a non-`20x` status code. (`#17`_)

Deprecated
^^^^^^^^^^
* ``krakenex.API.set_connection()`` method. Access ``krakenex.API.conn``
  attribute directly.

Known issues
^^^^^^^^^^^^
* There is no straightforward way to reset the ``krakenex.API`` object's
  connection ``krakenex.API.conn``. (`#53_`)

The recommended workaround for now, assuming ``k = krakenex.API()``:

.. code-block:: sh

   k.conn.close()
   k.conn = None

If a connection is not closed prior to the reference being removed, the
connection may continue to linger, preventing removal of the object by
the garbage collector.

.. _#17: https://github.com/veox/python3-krakenex/pull/17
.. _#53: https://github.com/veox/python3-krakenex/issues/53

[v1.0.0c1] - 2017-09-11 (Monday)
--------------------------------

**Release candidate.** Not recommended for production use.

Added
^^^^^
* Minimal Travis CI integration_. (`#45`_)

.. _integration: https://travis-ci.org/veox/python3-krakenex
.. _#45: https://github.com/veox/python3-krakenex/issues/45

[v1.0.0a1] - 2017-08-04 (Friday)
--------------------------------

**Internal alpha testing release!** Not for general use. For that
reason, ``pip`` package not provided.

Changed
^^^^^^^
* Cleaned up examples.

[v1.0.0a0] - 2017-07-02 (Sunday)
--------------------------------

**Internal alpha testing release!** Not for general use. For that
reason, ``pip`` package not provided.

Added
^^^^^
* More examples.

Changed (breaking!)
^^^^^^^^^^^^^^^^^^^
* Low-level ``Connection._request`` now raises
  ``http.client.HTTPException`` if response doesn't have ``20x``
  status code. This propagates all the way up, to
  ``API.query_{private,public}``. (`#17`_)

Changed
^^^^^^^
* Fix new connection thrashing if one is not provided for reuse
  (as was described in the docs). (`#27`_)
* Be explicit when using default arguments in functions that have
  optional ones. (`#19`_)
* Renamed ``NEWS`` to ``CHANGELOG``.

Deprecated
^^^^^^^^^^
* ``krakenex.API.set_connection()`` method. Access ``krakenex.API.conn``
  attribute directly.

.. _#17: https://github.com/veox/python3-krakenex/pull/17
.. _#19: https://github.com/veox/python3-krakenex/issues/19
.. _#27: https://github.com/veox/python3-krakenex/issues/27

[v0.1.4] - 2017-03-27 (Monday)
------------------------------

Changed
^^^^^^^
* Properly release key file descriptor after reading in key. (`#7`_)
* Verbose docs, served at ``https://python3-krakenex.readthedocs.io/``.

.. _#7: https://github.com/veox/python3-krakenex/pull/17

[v0.1.3] - 2017-01-31 (Tuesday)
-------------------------------
  
Changed
^^^^^^^
* Single-source version and URL - used during setup and in
  ``User-Agent``. (`#5`_)

.. _#5: https://github.com/veox/python3-krakenex/issues/5

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
* Now available on `PyPI`_ as a source distribution. (`#3`_)

.. _PyPI: https://pypi.python.org/pypi/krakenex
.. _#3: https://github.com/veox/python3-krakenex/issues/3

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
