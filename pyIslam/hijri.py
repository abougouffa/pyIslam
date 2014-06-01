# -*- coding: utf-8 -*-

from datetime import date, timedelta
from pyIslam.baselib import *


class HijriDate:
    def __init__(self, year, month, day):  # Constructor
        if (type(year) is int) and (type(month) is int) and (type(day) is int):
            if year < 0:
                raise Exception('Year < 0')
            else:
                self.year = year

            if month < 0:
                raise Exception('Month < 0')
            elif month > 12:
                raise Exception('Month > 12')
            else:
                self.month = month

            if day < 0:
                raise Exception('Day < 0')
            elif day > 30:
                raise Exception('Day > 30')
            else:
                self.day = day
        else:
            raise Exception('The day, month and year values must be integers')

    def __sub__(self, value):  # Return date dalta, self - value
        if isinstance(value, HijriDate):
            return timedelta(hijriToJulianDay(self) - hijriToJulianDay(value))
        else:
            raise TypeError("unsupported operand type(s) for -: %s and %s"
                            % (str(type(self)), str(type(value))))

    def today(correction_val=0):
        return HijriDate.getHijri(date.today(), correction_val)

    def getHijri(dat, correction_val=0):
        if isinstance(dat, date):
            hijri = HijriDate(0, 0, 0)
            hd = getHijriDate(gregorianToJulianDay(dat), correction_val)
            hijri.year, hijri.month, hijri.day = hd[0], hd[1], hd[2]
            return hijri
        else:
            raise Exception('dat is not a date object')

    def toGregorian(self):
        return getGregorianDate(hijriToJulianDay(self))

    def format(self, lang=0):
        '''lang: 1 = Arabic, 2: English, without = Numeric'''

        month_name = {1: (u'محرم',
                          u'صفر',
                          u'ربيع الأول',
                          u'ربيع الثاني',
                          u'جمادى الأولى',
                          u'جمادى الثانية',
                          u'رجب',
                          u'شعبان',
                          u'رمضان',
                          u'شوال',
                          u'ذو القعدة',
                          u'ذو الحجة'),
                      2: ('Moharram',
                          'Safar',
                          'Rabie-I',
                          'Rabie-II',
                          'Jumada-I',
                          'Jumada-II',
                          'Rajab',
                          'Shaban',
                          'Ramadan',
                          'Shawwal',
                          'Delqada',
                          'Delhijja')}

        if lang == 0:  # Numeric Format
            return '%02d-%02d-%04d' % (self.day, self.month, self.year)

        return (str(self.day) + ' '
                + month_name[lang][self.month - 1]
                + ' ' + str(self.year))
