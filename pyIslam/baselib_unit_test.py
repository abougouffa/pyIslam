# -*- coding: utf-8 -*-

from math import cos, sin, pi, ceil, floor
from datetime import date, datetime
from pyIslam.baselib import *

# Warning: These tests can fail if you are using on Python2!
assert gregorian_to_julian(datetime(1957, 10, 4, 19, 26, 24)) == 2436116.31
assert gregorian_to_julian(datetime(333, 1, 27, 12, 00, 00)) == 1842713.0
assert gregorian_to_julian(datetime(2000, 1, 1, 12, 00, 00)) == 2451545.0
assert gregorian_to_julian(date(1600, 1, 1)) == 2305447.5
assert gregorian_to_julian(date(1900, 1, 1)) == 2415020.5

# Todo: use an internal type for date/datetime, to add support of negative years
# but actually, it is not important because in our library we don't care about
# negative years!
# assert gregorian_to_julian(datetime(-1000, 7, 12, 12)) == 1356001.0
