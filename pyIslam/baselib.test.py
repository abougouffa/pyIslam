# -*- coding: utf-8 -*-

from math import cos, sin, pi, ceil, floor
from datetime import date
from baselib import *

assert gregorian_to_julian(date(2000, 1, 1)) == 2451545
assert gregorian_to_julian(date(1996, 3, 31)) == 2450174