Release checklist
=================

Pre-release
-----------
* Can expect to be generally available for the next month.
* Checked that there are no FIXMEs in the code, including docstrings.
* Have checked for TODOs in the code, and found them small enough to
  delay resolution.
* There are no open issues for this release on github.
* Have checked the package locally (installation, docgen, etc.).

Release
-------
* Built and pushed test PyPI package to testpypi.python.org.
* Tagged and signed commit, pushed to github.
* Built and pushed actual PyPI package.
* Triggered doc rebuild on readthedocs.io.

Post-release
------------
* Announce, issue API change warnings if required.
