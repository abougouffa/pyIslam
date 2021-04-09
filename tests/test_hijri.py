# -*- coding: utf-8 -*-

from datetime import date, datetime
from pyIslam.hijri import HijriDate


def test_hijri():
    hijri_date = HijriDate(1442, 8, 25)
    tomorrow = hijri_date.next_date()
    gregorian = hijri_date.to_gregorian()
    hijri_from_gregorian = hijri_date.get_hijri(date(2021, 4, 9))
    hijri_from_julian = hijri_date.from_julian(2459313)

    assert hijri_date.format() == "25-08-1442"
    # FIXME according to https://www.islamicfinder.org/islamic-calendar/
    # it should be 27 Shaban 1442
    assert hijri_date.format(2) == "25 Shaban 1442"
    assert tomorrow.format() == "26-08-1442"
    assert tomorrow.format(2) == "26 Shaban 1442"

    assert gregorian == date(2021, 4, 13)

    assert hijri_from_gregorian.format(2) == "25 Shaban 1442"
    assert hijri_from_julian.format(2) == "25 Shaban 1442"
