Release checklist
=================

Pre-release
-----------
* Can expect to be generally available for the next month.
* Travis builds are passing.
* Checked that there are no FIXMEs in the code, including docstrings.
* Have checked for TODOs in the code, and found them small enough to
  delay resolution.
* There are no open issues for this release on github.
* Have checked the package locally (installation, docgen, etc.).
* Changes are documented and migration instructions present in CHANGELOG.

Release
-------
* Bump version.
* Update changelog.
* Build package.

.. code-block:: sh

   python ./setup.py build
   python ./setup.py sdist

* Push test PyPI package to testpypi.python.org.

.. code-block:: sh

   twine upload --repository testpypi dist/krakenex-X.Y.Z.tar.gz

* Commit changes.

* Tagged and signed commit, pushed to github.

.. code-block:: sh

   git tag -u 1298BC0A9B0DBEEA3BDDCBA62D3DA6CD74AB3D37 -s vX.Y.Z
   git push -v
   git push -v --tags

* Push actual PyPI package.

.. code-block:: sh

   twine upload --repository pypi dist/krakenex-X.Y.Z.tar.gz

* Doc rebuild has triggered on readthedocs.io.

Post-release
------------
* Announce, issue API change warnings if required.
