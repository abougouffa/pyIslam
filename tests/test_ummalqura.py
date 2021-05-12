# -*- coding: utf-8 -*-

from datetime import date, datetime
from pyIslam.ummalqura import UmmAlQuraCalendar


def test_ummalqura():
    hijri_date = UmmAlQuraCalendar(2021, 5, 1)  # HijriDate(1442, 8, 25)

    print(hijri_date.week_day)
    print(hijri_date.hijri_date)
    print(hijri_date.greg_date)
    print(hijri_date.solar_hijri_date)
    print(hijri_date.islamic_lunation_num)
    print(hijri_date.islamic_month_length)


test_ummalqura()
