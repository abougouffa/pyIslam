# -*- coding: utf-8 -*-

from datetime import date, datetime
from pyIslam.baselib import (
    gregorian_to_julian,
    dcos,
    dsin,
    equation_of_time,
    hijri_to_julian,
    julian_to_hijri,
    julian_to_gregorian,
)


def test_dcos():
    assert dcos(10) == 0.984807753012208
    assert dcos(20) == 0.9396926207859084
    assert dcos(30) == 0.8660254037844387


def test_dsin():
    assert dsin(10) == 0.17364817766693033
    assert dsin(20) == 0.3420201433256687
    assert dsin(30) == 0.49999999999999994


def test_equation_of_time():
    assert equation_of_time(2436116.31) == -11.671836528931657
    assert equation_of_time(1842713.0) == 12.957933162396277
    assert equation_of_time(2451545.0) == 3.5355137428081367


def test_hijri_to_julian():
    assert hijri_to_julian(date(1442, 8, 25)) == 2459313
    assert hijri_to_julian(date(333, 1, 27)) == 2066116
    assert hijri_to_julian(date(1, 1, 27)) == 1948466


def test_gregorian_to_julian():
    assert gregorian_to_julian(datetime(1957, 10, 4, 19, 26, 24)) == 2436116.31
    assert gregorian_to_julian(datetime(333, 1, 27, 12, 00, 00)) == 1842713.0
    assert gregorian_to_julian(datetime(2000, 1, 1, 12, 00, 00)) == 2451545.0
    assert gregorian_to_julian(date(1600, 1, 1)) == 2305447.5
    assert gregorian_to_julian(date(1900, 1, 1)) == 2415020.5


# Todo: use an internal type for date/datetime, to add support of negative years
# but actually, it is not important because in our library we don't care about
# negative years!
# assert gregorian_to_julian(datetime(-1000, 7, 12, 12)) == 1356001.0


def test_julian_to_hijri():
    assert julian_to_hijri(2459313) == (1442, 8, 25)
    assert julian_to_hijri(2066116.0) == (333, 1, 27)
    assert julian_to_hijri(1948466.0) == (1, 1, 27)


def test_julian_to_gregorian():
    assert julian_to_gregorian(2459313) == (2021, 4, 13)
    assert julian_to_gregorian(2415020.5) == (1900, 1, 5.5)
