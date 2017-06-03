# -*- coding: utf-8 -*-

from math import cos, sin, pi, ceil, floor
from datetime import date


# Trigonometric functions takes values in degree
def dcos(deg):
    return cos((deg * pi) / 180)


def dsin(deg):
    return sin((deg * pi) / 180)

# Hijri date calculation methods
def hijri_to_julian(dat):
    return (floor((11 * dat.year + 3) / 30)
            + floor(354 * dat.year)
            + floor(30 * dat.month)
            - floor((dat.month - 1) / 2)
            + dat.day + 1948440 - 385)


def gregorian_to_julian(dat):  # Julian Day
    if dat is None:
        dat = date.today()

    day = dat.day
    month = dat.month
    year = dat.year

    if month == 1 or month == 2:
        month = month + 12
        year = year - 1

    a = floor(year / 100)
    b = 0

    if year > 1582 or (year == 1582 and (month > 10 or (month == 10 and day > 15))):
        # If it is a gregorian calendar set b
        b = 2 - a + floor(a / 4)

    return ceil(floor(365.25 * (year + 4716))
            + floor(30.6001 * (month + 1))
            + day + b - 1524.5)


def julian_to_hijri(julian_day, correction_val=0):
    l = floor(julian_day + correction_val) - 1948440 + 10632
    n = floor((l - 1) / 10631)
    l = l - 10631 * n + 354
    j = (floor((10985 - l) / 5316) * floor((50 * l) / 17719)
         + floor(l / 5670) * floor((43 * l) / 15238))
    l = (l - floor((30 - j) / 15) * floor((17719 * j) / 50)
         - floor(j / 16) * floor((15238 * j) / 43) + 29)
    month = floor((24 * l) / 709)
    day = l - floor((709 * month) / 24)
    year = floor(30 * n + j - 30)
    return (year, month, day)


def julian_to_gregorian(jd):
    z = floor(jd)
    f = jd - z

    if z < 2299161:
        a = z
    else:
        alpha = floor((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - floor((alpha / 4))

    b = a + 1524
    c = floor((b - 122.1) / 365.25)
    d = floor(365.25 * c)
    e = floor((b - d) / 30.6001)

    # Calculate the day
    day = b - d - floor(30.6001 * e) + f

    # Calculate the month
    if e < 14:
        month = e - 1
    elif e == 14 or e == 15:
        month = e - 13

    # Calculate the year
    if month > 2:
        year = c - 4716

    elif month == 1 or month == 2:
        year = c - 4715

    return (year, month, day)
