#!/usr/bin/env python

import os.path
from distutils.core import setup
from krakenex.version import __url__, __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='krakenex',
      version=__version__,
      description='kraken.com cryptocurrency exchange API',
      long_description=read('README.rst'),
      author='Noel Maersk',
      author_email='veox+packages+spamremove@veox.pw',
      url=__url__,
      install_requires=read("requirements.txt").splitlines(),
      packages=['krakenex'],
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ]
)
