# -*- coding: utf-8 -*-

from math import *
from datetime import date, time
from pyIslam.hijri import *
from pyIslam.baselib import *

class PrayerConf:
    def __init__(self, longitude, latitude, timezone, zenith_ref=3, asr_madhab=1, enable_summer_time=False):
        '''Initialize the PrayerConf object
        @param longitude: geographical longitude of the given location
        @param latitude: geographical latitude of the given location
        @param timezone: the time zone GMT(+/-X)
        @param zenith_ref: integer value for the Fajr and Ishaa zenith angle reference
        1 = University of Islamic Sciences, Karachi
        2 = Muslim World League
        3 = Egyptian General Authority of Survey (default)
        4 = Umm al-Qura University, Makkah
        5 = Islamic Society of North America
        @param asr_madhab: integer value
        1 = Shafii (default)
        2 = Hanafi
        @param: enable_summer_time: True if summer time is used in the place, False (default) if not'''

        self.longitude = longitude
        self.latitude = latitude
        self.timezone = timezone
        self.sherookZenith = 90.83333 # Constants
        self.maghrebZenith = 90.83333

        if asr_madhab == 2:
            self.asrMadhab = asr_madhab # 1 = Shafii (Default), 2 = Hanafi
        else: self.asrMadhab = 1

        self.middleLongitude = self.timezone * 15
        self.longitudeDifference = (self.middleLongitude - self.longitude) / 15

        if enable_summer_time: self.summerTime = 1
        else: self.summerTime = 0

        if zenith_ref == 1:   # 1 = University of Islamic Sciences, Karachi
            self.fajrZenith = 108.0     # 90 + 18.0
            self.ishaaZenith = 108.0    # 90 + 18.0
        elif zenith_ref == 2: # 2 = Muslim World League
            self.fajrZenith = 108.0     # 90 + 18.0
            self.ishaaZenith = 107.0    # 90 + 17.0
        elif zenith_ref == 3: # 3 = Egyptian General Authority of Survey (default)
            self.fajrZenith = 109.5     # 90 + 19.5
            self.ishaaZenith = 107.5    # 90 + 17.5
        elif zenith_ref == 4: # 4 = Umm al-Qura University, Makkah
            self.fajrZenith = 108.5     # 90 + 18.5
            self.ishaaZenith = 0.0      # 90 minutes after the maghreb time (or 120 minutes in Ramadan only)
        elif zenith_ref == 5: # 5 = Islamic Society of North America
            self.fajrZenith = 105.0     # 90 + 15.0
            self.ishaaZenith = 105.0    # 90 + 15.0


class Prayer: # Prayer times and qiblah calculating class
    def __init__(self, conf, dat):
        self.__conf=conf
        self.__date=dat

    def __equationOfTime(self): # Get equation of time
        n = gregorianToJulianDay(self.__date) - 2451544.5
        g = 357.528 + 0.9856003 * n
        c = 1.9148 * dsin(g) + 0.02 * dsin(2 * g) + 0.0003 * dsin(3 * g)
        lamda = 280.47 + 0.9856003 * n + c
        r = -2.468 * dsin(2 * lamda) + 0.053 * dsin(4 * lamda) + 0.0014 * dsin(6 * lamda)
        return (c + r) * 4


    def __asrZenith(self): # Get the zenith angle for asr pray (according to choosed asr religion)
        delta = self.__sunDeclination()
        x = dsin(self.__conf.latitude) * dsin(delta) + dcos(self.__conf.latitude) * dcos(delta)
        a = atan(x / sqrt(-x * x + 1))
        x = self.__conf.asrMadhab + (1 / tan(a))
        return 90 - (180 / pi) * (atan(x) + 2 * atan(1))


    def __sunDeclination(self): # Get sun declination
        n = gregorianToJulianDay(self.__date) - 2451544.5
        epsilon = 23.44 - 0.0000004 * n
        l = 280.466 + 0.9856474 * n
        g = 357.528 + 0.9856003 * n
        lamda = l + 1.915 * dsin(g) + 0.02 * dsin(2 * g)
        x = dsin(epsilon) * dsin(lamda)
        return (180 / (4 * atan(1))) * atan(x / sqrt(-x * x + 1))


    def fajrTime(self): # Fajr Time
        '''Get the Fajr time'''
        return Prayer._Prayer__hoursToTime(self.__dohrTime() - self.__prayerTime(self.__conf.fajrZenith))


    def sherookTime(self): # Sherook Time
        '''Get the Sunrise (Sherook) time'''
        return Prayer._Prayer__hoursToTime(self.__dohrTime() - self.__prayerTime(self.__conf.sherookZenith))


    def __dohrTime(self): # Dohr time for internal use, return number of hours, not time object
        '''Get the Dohr time'''
        ld = self.__conf.longitudeDifference
        time_eq = self.__equationOfTime()
        duhr_t = 12 + ld + time_eq / 60
        return duhr_t


    def dohrTime(self): # Dohr Time
        return Prayer._Prayer__hoursToTime(self.__dohrTime())


    def asrTime(self): # Asr Time
        '''Get the Asr time'''
        return Prayer._Prayer__hoursToTime(self.__dohrTime() + self.__prayerTime(self.__asrZenith()))


    def maghrebTime(self): # Maghreb Time
        '''Get the Maghreb time'''
        return Prayer._Prayer__hoursToTime(self.__dohrTime() + self.__prayerTime(self.__conf.maghrebZenith))


    def ishaaTime(self): # ishaa Time
        '''Get the Ishaa time'''
        if (self.__conf.ishaaZenith == 0.0):
            hij = today(1)
            if (hij.month == 9):
                ishaa_t = self.maghreb_time() + 2.0 # 2.0 hours = 120 minutes
            else:
                ishaa_t = self.maghreb_time() + 1.5 # 1.5 hours = 90 minutes
        else:
            ishaa_t = self.__prayerTime(self.__conf.ishaaZenith)
            ishaa_t = self.__dohrTime() + ishaa_t
        return Prayer._Prayer__hoursToTime(ishaa_t)


    def __prayerTime(self, zenith): # Get Times for "Fajr, Sherook, Asr, Maghreb, ishaa"
        delta = self.__sunDeclination()
        s = (dcos(zenith) - dsin(self.__conf.latitude) * dsin(delta)) / (dcos(self.__conf.latitude) * dcos(delta))
        return (180 / pi * (atan(-s / sqrt(-s * s + 1)) + pi / 2)) / 15


    def __hoursToTime(val, summer_time = False): # Convert a decimal value (in hours) to time object
        if summer_time: st = 1
        else: st = 0
        hours = val
        minutes = (hours - int(hours)) * 60
        seconds = (minutes - int(minutes)) * 60
        return time((int(hours) + st), int(minutes), int(seconds))
