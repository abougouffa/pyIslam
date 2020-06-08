# -*- coding: utf-8 -*-

# SOME REFERENCES FOR USED ALGORITHMS (for more info see docs/References.md)
# [3]: Meeus, Jean, Astronomical Algorithms, ISBN:0-943396-35-2


from math import cos, sin, pi, ceil, floor
from datetime import date, datetime


# Trigonometric functions takes values in degree
def dcos(deg):
    return cos((deg * pi) / 180)


def dsin(deg):
    return sin((deg * pi) / 180)

# Hijri date calculation methods


def equation_of_time(jd):
    '''Get equation of time'''
    n = jd - 2451544.5
    g = 357.528 + 0.9856003 * n
    c = 1.9148 * dsin(g) + 0.02 * dsin(2 * g) + 0.0003 * dsin(3 * g)
    lamda = 280.47 + 0.9856003 * n + c
    r = (-2.468 * dsin(2 * lamda)
         + 0.053 * dsin(4 * lamda)
         + 0.0014 * dsin(6 * lamda))
    return (c + r) * 4


def hijri_to_julian(dat):
    return (floor((11 * dat.year + 3) / 30)
            + floor(354 * dat.year)
            + floor(30 * dat.month)
            - floor((dat.month - 1) / 2)
            + dat.day + 1948440 - 385)


def gregorian_to_julian(dat):
    '''
    The Julian Day (JD) is a continuous count of days and fractions from the beginning of the year -4712,
    I begins at Greenwich mean noon (12h Universal Time)
    '''

    if dat is None:
        dat = datetime.now()

    day, month, year = dat.day, dat.month, dat.year

    # This method works also for fractions of a day, however, the `date` type doesn't
    # support the fractions in the day, an alternative is to pass the datetime and the
    # time will be converted to a fraction of a day
    if type(dat) is date:
        pass
    elif type(dat) is datetime:
        day += (dat.hour + (dat.minute + (dat.second / 60)) / 60.0) / 24.0

    if month <= 2:
        month = month + 12
        year = year - 1

    a = floor(year / 100)

    # In this method, the Gregorian calendar reform is taken into account, the day
    # following 04 Oct. 1582 (Julian calendar) is 15 Oct. 1582 (Gregorian calendar)
    # for more information see [3, p60]

    b = 2 - a + floor(a / 4) if year > 1582 or (year ==
                                                1582 and (month > 10 or (month == 10 and day > 15))) else 0

    # The corresponding Julian Day is:
    jd = floor(365.25 * (year + 4716)) + \
        floor(30.60  # In Python3, 30.6 gives a right result, no need to use 30.6001 as described in [3, p61]
              * (month + 1)) + day + b - 1524.5
    return jd


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
    jd = jd + 5
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
    e = floor((b - d) / 30.6001)  # The 30.6001 SHOULD NOT BE REPLACED by 30.6

    # Calculate the day
    day = b - d - floor(30.6001 * e) + f

    # Calculate the month
    month = e - (1 if e < 14 else 13)

    # Calculate the year
    year = c - (4716 if month > 2 else 4715)

    return (year, month, day)
