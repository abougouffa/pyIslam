#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Hijri Organizer is a free islamic organizer
Copyright © 2010 Abdelhak Mohammed Bougouffa (abdelhak@cryptolab.net)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
'''

from math import cos, sin, pi
from datetime import date

# Trigonometric functions takes values in degree
def dcos(deg): return cos((deg * pi) / 180)
def dsin(deg): return sin((deg * pi) / 180)

# Hijri date calculation methods
def hijriToJulianDay(dat):
    return int((11 * dat.year + 3) / 30) + int(354 * dat.year) + int(30 * dat.month) - int((dat.month - 1) / 2) + dat.day + 1948440 - 385


def gregorianToJulianDay(dat): # Julian Day
    is_julian_org = False
    is_gregorian_org = False
    day = dat.day
    month = dat.month
    year = dat.year

    if (dat == None):
        dat = date.today()

    if (year > 1582):
        is_gregorian_org = True
    elif (year < 1582):
        is_julian_org = True
    elif (year == 1582):
        if (month > 10):
            is_gregorian_org = True
        elif (month < 10):
            is_julian_org = True
        elif (month == 10):
            if (day > 15):
                is_gregorian_org = True
            elif (day <= 15):
                is_julian_org = True

    if (month == 1 or month == 2):
        month = month + 12
        year = year - 1

    a = int(year / 100)
    b = 0

    if (is_gregorian_org):
        b = 2 - a + int(a / 4)
    elif (is_julian_org):
        b = 0

    return int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5 # Julian Day


def getHijriDate(julian_day, correction_val = 0):
    l = int(julian_day + correction_val) - 1937808
    n = int((l - 1) / 10631)
    l = l - 10631 * n + 354
    j = int((10985 - l) / 5316) * int((50 * l) / 17719) + int(l / 5670) * int((43 * l) / 15238)
    l = l - int((30 - j) / 15) * int((17719 * j) / 50) - int(j / 16) * int((15238 * j) / 43) + 29
    month = int((24 * l) / 709)
    day = l - int((709 * month) / 24)
    year = int(30 * n + j - 30)
    return (year, month, day)


def getGregorianDate(jd):

	z = int(jd)
	f = jd - z;
	
	if z < 2299161:
		a = z
	else:
		alpha = int((z - 1867216.25) / 36524.25)
		a = z + 1 + alpha - int((alpha / 4))
	
	b = a + 1524
	c = int((b - 122.1) / 365.25)
	d = int(365.25 * c)
	e = int((b - d) / 30.6001)
	
	# Calculate the day
	day = b - d - int(30.6001 * e) + f
	
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
