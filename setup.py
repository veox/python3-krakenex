#!/usr/bin/env python3

import os.path
from distutils.core import setup

exec(open('./krakenex/version.py').read())

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='krakenex',
      version=__version__,
      description='kraken.com cryptocurrency exchange API',
      long_description=read('README.rst'),
      author='Noel Maersk',
      author_email='veox+packages+spamremove@veox.pw',
      url=__url__,
      install_requires=[
          'requests>=2.18.2,<3'
      ],
      packages=['krakenex'],
      python_requires='>=3.3',
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
)
