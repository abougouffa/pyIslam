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


from datetime import date, time
from baselib import *

class HijriDate:
    year = 0
    month = 0
    day = 0
    

    def __init__(self, year, month, day): # Constructor
        if (type(year) is int) and (type(month) is int) and (type(day) is int):
            if year < 0: raise Exception('Year < 0')
            else: self.year = year

            if month < 0: raise Exception('Month < 0')
            elif month > 12: raise Exception('Month > 12')
            else: self.month = month

            if day < 0: raise Exception('Day < 0')
            elif day > 30: raise Exception('Day > 30')
            else: self.day = day
        else: raise Exception('The day, month and year values must be integers')
    
    @staticmethod
    def today(correction_val = 0):
        return getHijriDate(gregorianToJulianDay(date.today()), correction_val)


    def format(self, lang = 0):
        '''lang: 1 = Arabic, 2: English, without = Numeric'''

        if (lang == 0): # Numeric Format
            if (self.day > 9): str_day = str(self.day)
            else: str_day = '0' + str(self.day)
            if (self.month > 9): str_month = str(self.month)
            else: str_month = '0' + str(self.month)
            if (self.year > 999): str_year = str(self.year)
            elif (self.year > 99): str_year = '0' + str(self.year)
            elif (self.year > 9): str_year = '00' + str(self.year)
            else: str_year = '000' + str(self.year)
            str_date = str_day + '-' + str_month + '-' + str_year

        elif (lang == 1): # Arabic Language
            if (self.month == 1): month_name = u'محرم'
            elif (self.month == 2): month_name = u'صفر'
            elif (self.month == 3): month_name = u'ربيع الأول'
            elif (self.month == 4): month_name = u'ربيع الثاني'
            elif (self.month == 5): month_name = u'جمادى الأولى'
            elif (self.month == 6): month_name = u'جمادى الثانية'
            elif (self.month == 7): month_name = u'رجب'
            elif (self.month == 8): month_name = u'شعبان'
            elif (self.month == 9): month_name = u'رمضان'
            elif (self.month == 10): month_name = u'شوال'
            elif (self.month == 11): month_name = u'ذو القعدة'
            elif (self.month == 12): month_name = u'ذو الحجة'
            str_date = str(self.day) + ' ' + month_name + ' ' + str(self.year)

        elif (lang == 2): # English Language
            if (self.month == 1): month_name = 'Moharram'
            elif (self.month == 2): month_name = 'Safar'
            elif (self.month == 3): month_name = 'Rabie-I'
            elif (self.month == 4): month_name = 'Rabie-II'
            elif (self.month == 5): month_name = 'Jumada-I'
            elif (self.month == 6): month_name = 'Jumada-II'
            elif (self.month == 7): month_name = 'Rajab'
            elif (self.month == 8): month_name = 'Shaban'
            elif (self.month == 9): month_name = 'Ramadan'
            elif (self.month == 10): month_name = 'Shawwal'
            elif (self.month == 11): month_name = 'Delqada'
            elif (self.month == 12): month_name = 'Delhijja'
            str_date = str(self.day) + ' ' + month_name + ' ' + str(self.year)

        return str_date
