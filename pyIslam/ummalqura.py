import math
from .ummalqura_table import *

# Ported form https://webspace.science.uu.nl/~gent0113/islam/addfiles/ummalqura_calendar.js

# def gmod(n, m):
#     #  generalized  modulo  function  (n  mod  m)  also  valid  for  negative  values  of  n
#     return ((n % m) + m) % m


class UmmAlQuraCalendar:
    def __init__(self, year, month, day):
        #  read  calendar  data
        m = month  # + 1
        y = year

        #  append  January  and  February  to  the  previous  year  (i.e.  regard  March  as
        #  the  first  month  of  the  year  in  order  to  simplify  leap  day  corrections)
        if m < 3:
            y -= 1
            m += 12

        #  compute  offset  between  Julian  and  Gregorian  calendar
        a = math.floor(y / 100.0)
        jgc = a - math.floor(a / 4.0) - 2

        #  compute  Chronological  Julian  Day  Number  (CJDN)
        cjdn = (
            math.floor(365.25 * (y + 4716))
            + math.floor(30.6001 * (m + 1))
            + day
            - jgc
            - 1524
        )

        a = math.floor((cjdn - 1867216.25) / 36524.25)
        jgc = a - math.floor(a / 4.0) + 1
        b = cjdn + jgc + 1524
        c = math.floor((b - 122.1) / 365.25)
        d = math.floor(365.25 * c)
        month = math.floor((b - d) / 30.6001)
        day = (b - d) - math.floor(30.6001 * month)

        if month > 13:
            c += 1
            month -= 12

        month -= 1
        year = c - 4716

        #  compute  weekday
        wd = ((cjdn + 1) % 7) + 1  # gmod(cjdn + 1, 7) + 1

        #  output  Western  calendar  date  and  weekday
        self.greg_date = (year, month, day)
        self.week_day = wd  # -1

        #  output  Chronological  Julian  Day  Number  and  weekday
        self.julian_day = cjdn

        #  compute  Modified  Chronological  Julian  Day  Number  (MCJDN)
        mcjdn = cjdn - 2400000

        #  the  MCJDN's  of  the  start  of  the  lunations  in  the  Umm  al-Qura  calendar  are  stored  in  'islamcalendar_dat.js'
        i = 0
        for k in range(len(UMMALQURA_TABLE)):
            i = k
            if UMMALQURA_TABLE[k] > mcjdn:
                break

        #  compute  and  output  the  Umm  al-Qura  calendar  date
        iln = i + 16260
        ii = math.floor((iln - 1) / 12)
        iy = ii + 1
        im = iln - 12 * ii
        id = mcjdn - UMMALQURA_TABLE[i - 1] + 1
        ml = UMMALQURA_TABLE[i] - UMMALQURA_TABLE[i - 1]

        self.hijri_date = (iy, im, id)

        #  compute  the  solar  Hijri  date
        epoch = 450947 + jgc

        sy = math.floor((mcjdn + epoch) / 365.25)
        sd = (mcjdn + epoch) - math.floor(365.25 * sy)

        if sd < 186.5:
            sm = math.floor(sd / 31.0001)
            sd = sd - math.floor(31.0001 * sm)
            sm = sm + 6
        else:
            sy = sy + 1
            sm = math.floor((sd - 186) / 30.0001)
            sd = (sd - 186) - math.floor(30.0001 * sm)

        #  fix  for  leap  day  in  Gregorian  leap  year
        if sd == 0 and sm == 6:
            sd = 30
            sm = 5

        #  output  Islamic  solar  date
        self.solar_hijri_date = (sy + 2, sm, sd)

        #  output  Islamic  lunation  number  and  month  length
        self.islamic_lunation_num = iln
        self.islamic_month_length = ml
