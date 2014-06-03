# -*- coding: utf-8 -*-

from datetime import date, timedelta
from pyIslam.baselib import (getHijriDate, gregorianToJulianDay,
                             hijriToJulianDay, getGregorianDate)


class HijriDate:
    def __init__(self, year, month, day):  # Constructor
        if isinstance(year, int):
            if year < 0:
                raise ValueError('year must be positive')
            else:
                self.year = year
        else:
            raise TypeError('year must be an int')

        if isinstance(month, int):
            if not (month in range(1, 13)):
                raise ValueError('month should be bitween 1 and 12')
            else:
                self.month = month
        else:
            raise TypeError('month must be an int')

        if isinstance(day, int):
            if not (month in range(1, 31)):
                raise ValueError('day should be bitween 1 and 30')
            else:
                self.day = day
        else:
            raise TypeError('day must be an int')

        self.__julian = hijriToJulianDay(self)

    def __sub__(self, value):  # Return date dalta, self - value
        if isinstance(value, HijriDate):
            return timedelta(self.__julian - hijriToJulianDay(value))
        else:
            raise TypeError("unsupported operand type(s) for -: %s and %s"
                            % (str(type(self)), str(type(value))))

    def today(correction_val=0):
        return HijriDate.getHijri(date.today(), correction_val)

    def fromJulian(jd, correction_val=0):
        hd = getHijriDate(jd, correction_val)
        return HijriDate(hd[0], hd[1], hd[2])

    def getHijri(dat, correction_val=0):
        '''get hijri date from gregorian date "dat"'''
        if isinstance(dat, date):
            hd = getHijriDate(gregorianToJulianDay(dat), correction_val)
            return HijriDate(hd[0], hd[1], hd[2])
        else:
            raise TypeError("dat is not a 'date' object")

    def toGregorian(self):
        gd = getGregorianDate(self.__julian)
        return date(gd[0], gd[1], gd[2])

    def nextDate(self):
        return HijriDate.fromJulian(self.__julian + 1)

    def isLast(self):
        if self.month != self.nextDate().month:
            return True
        else:
            return False

    def format(self, lang=0):
        '''lang: 1 = Arabic, 2: English, without = Numeric'''

        if not isinstance(lang, int):
            raise TypeError('lang should be an int')
        elif not (lang in range(0, 3)):
            raise ValueError('lang should be bitween 0 and 2')

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

        return '%s %s %s' % (str(self.day), month_name[lang][self.month - 1],
                             str(self.year))
