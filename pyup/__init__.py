"""PyUp - Markup generation tool.

:copyright: Copyright (c) 2015 by Robert Pogorzelski.
:license:   MIT, see LICENSE for more details.

"""
from pyup.base import *
from pyup.elements import *


VERSION = (1, 0, 0)


__version__ = ".".join(map(str, VERSION[0:3])) + "".join(VERSION[3:])
__author__ = "Robert Pogorzelski <thinkingpotato@gmail.com>"
__docformat__ = "restructuredtext"
