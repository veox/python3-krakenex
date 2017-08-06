# This file is part of krakenex.
#
# krakenex is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# krakenex is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser
# General Public LICENSE along with krakenex. If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt>.


""" General-use interface provided by `krakenex`.

Internally, classes are in separate modules, but they are also exported
to the top-level namespace, so the following uses are possible:

.. code-block:: python

   # recommended, unlikely to result in namespace collisions
   import krakenex
   k = krakenex.API()
   c = krakenex.Connection()

   # OK for simple scripts
   from krakenex import *
   k = API()
   c = Connection()

   # can be explicit in both cases
   k = krakenex.api.API()
   c = krakenex.connection.Connection()

"""

# "public interface"
from .api import API
from .connection import Connection
from .response import Response
__all__ = ['API', 'Connection']
