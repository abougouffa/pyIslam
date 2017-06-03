# -*- coding: utf-8 -*-

from math import pi, atan, sqrt, tan, floor
from datetime import time
from pyIslam.hijri import HijriDate
from pyIslam.baselib import dcos, dsin, gregorian_to_julian
from math import *


class PrayerConf:
    def __init__(self, longitude, latitude, timezone, zenith_ref=3,
                 asr_madhab=1, enable_summer_time=False):
        '''Initialize the PrayerConf object
        @param longitude: geographical longitude of the given location
        @param latitude: geographical latitude of the given location
        @param timezone: the time zone GMT(+/-timezone)
        @param zenith_ref: integer value for the Fajr and
        Ishaa zenith angle reference
        1 = University of Islamic Sciences, Karachi
        2 = Muslim World League
        3 = Egyptian General Authority of Survey (default)
        4 = Umm al-Qura University, Makkah
        5 = Islamic Society of North America
        @param asr_madhab: integer value
        1 = Shafii (default)
        2 = Hanafi
        @param: enable_summer_time: True if summer time is used in the place,
        False (default) if not'''

        self.longitude = longitude
        self.latitude = latitude
        self.timezone = timezone
        self.sherook_zenith = 90.83333  # Constants
        self.maghreb_zenith = 90.83333

        if asr_madhab == 2:
            self.asr_madhab = asr_madhab  # 1 = Shafii, 2 = Hanafi
        else:
            self.asr_madhab = 1

        self.middle_longitude = self.timezone * 15
        self.longitude_difference = (self.middle_longitude - self.longitude) / 15

        self.summer_time = enable_summer_time

        zeniths = {1: (108.0, 108.0), # 1 = University of Islamic Sciences, Karachi
                   2: (108.0, 107.0), # 2 = Muslim World League
                   3: (109.5, 107.5), # 3 = Egyptian General Authority of Survey
                   4: (108.5, None),  # 4 = Umm al-Qura University, Makkah
                   5: (105.0, 105.0)} # 5 = Islamic Society of North America

        # Pythonista way to write switch-case instruction
        (self.fajr_zenith, self.ishaa_zenith) = zeniths.get(zenith_ref, zeniths[3])


class Prayer:
    '''Prayer times and qiblah calculating class'''
    def __init__(self, conf, dat, correction_val=0):
        self._conf = conf
        self._date = dat

        if not (correction_val in range(-2, 3)):
            raise Exception('Correction value exception')
        else:
            self._correction_val = correction_val

    def _equation_of_time(self):
        '''Get equation of time'''
        n = gregorian_to_julian(self._date) - 2451544.5
        g = 357.528 + 0.9856003 * n
        c = 1.9148 * dsin(g) + 0.02 * dsin(2 * g) + 0.0003 * dsin(3 * g)
        lamda = 280.47 + 0.9856003 * n + c
        r = (-2.468 * dsin(2 * lamda)
             + 0.053 * dsin(4 * lamda)
             + 0.0014 * dsin(6 * lamda))
        return (c + r) * 4
        # jd = gregorian_to_julian(self._date)
        # d = jd - 2451545.0

        # g = 357.529 + 0.98560028* d
        # q = 280.459 + 0.98564736* d
        # L = q + 1.915* dsin(g) + 0.020* dsin(2*g)

        # R = 1.00014 - 0.01671* dcos(g) - 0.00014* dcos(2*g)
        # e = 23.439 - 0.00000036* d
        # RA = atan2(dcos(e)* dsin(L), dcos(L))/ 15

        # D = asin(dsin(e)* dsin(L))# declination of the Sun
        # EqT = q/15.0 - RA# equation of time
        # return EqT

    def _asr_zenith(self):
        '''Get the zenith angle for asr (according to choosed asr fiqh)'''
        delta = self._sun_declination()
        x = (dsin(self._conf.latitude) * dsin(delta)
             + dcos(self._conf.latitude) * dcos(delta))
        a = atan(x / sqrt(-x * x + 1))
        x = self._conf.asr_madhab + (1 / tan(a))
        return 90 - (180 / pi) * (atan(x) + 2 * atan(1))

    def _sun_declination(self):
        '''Get sun declination'''
        n = gregorian_to_julian(self._date) - 2451544.5
        epsilon = 23.44 - 0.0000004 * n
        l = 280.466 + 0.9856474 * n
        g = 357.528 + 0.9856003 * n
        lamda = l + 1.915 * dsin(g) + 0.02 * dsin(2 * g)
        x = dsin(epsilon) * dsin(lamda)
        return (180 / (4 * atan(1))) * atan(x / sqrt(-x * x + 1))
        # jd = gregorian_to_julian(self._date)
        # d = jd - 2451545.0

        # g = 357.529 + 0.98560028* d
        # q = 280.459 + 0.98564736* d
        # L = q + 1.915* dsin(g) + 0.020* dsin(2*g)

        # R = 1.00014 - 0.01671* dcos(g) - 0.00014* dcos(2*g)
        # e = 23.439 - 0.00000036* d
        # RA = atan2(dcos(e)* dsin(L), dcos(L))/ 15

        # D = asin(dsin(e)* dsin(L))# declination of the Sun
        # EqT = q/15.0 - RA# equation of time
        # return D
    def _dohr_time(self):
        '''# Dohr time for internal use, return number of hours,
        not time object'''
        ld = self._conf.longitude_difference
        time_eq = self._equation_of_time()
        duhr_t = 12 + ld + time_eq / 60
        return duhr_t

    def _time(self, zenith):
        '''Get Times for "Fajr, Sherook, Asr, Maghreb, ishaa"'''
        delta = self._sun_declination()
        s = ((dcos(zenith)
              - dsin(self._conf.latitude) * dsin(delta))
             / (dcos(self._conf.latitude) * dcos(delta)))
        return (180 / pi * (atan(-s / sqrt(-s * s + 1)) + pi / 2)) / 15

    def _hours_to_time(val, shift, summer_time):
        '''Convert a decimal value (in hours) to time object'''
        if not (isinstance(shift, float) or isinstance(shift, int)):
            raise Exception("'shift' value must be an 'int' or 'float'")

        st = 1 if summer_time else 0

        hours = val + shift/3600
        minutes = (hours - floor(hours)) * 60
        seconds = (minutes - floor(minutes)) * 60
        return time((floor(hours) + st), floor(minutes), floor(seconds))

    def fajr_time(self, shift=0.0):
        '''Get the Fajr time'''
        return (Prayer._hours_to_time
                (self._dohr_time() - self._time(self._conf.fajr_zenith),
                 shift, self._conf.summer_time))

    def sherook_time(self, shift=0.0):
        '''Get the Sunrise (Sherook) time'''
        return (Prayer._hours_to_time
                (self._dohr_time()
                 - self._time(self._conf.sherook_zenith),
                 shift, self._conf.summer_time))

    def dohr_time(self, shift=0.0):
        return Prayer._hours_to_time(self._dohr_time(),
                                           shift, self._conf.summer_time)

    def asr_time(self, shift=0.0):
        '''Get the Asr time'''
        return (Prayer._hours_to_time
                (self._dohr_time() + self._time(self._asr_zenith()),
                 shift, self._conf.summer_time))

    def maghreb_time(self, shift=0.0):
        '''Get the Maghreb time'''
        return (Prayer._hours_to_time
                (self._dohr_time() + self._time
                 (self._conf.maghreb_zenith), shift, self._conf.summer_time))

    def ishaa_time(self, shift=0.0):
        '''Get the Ishaa time'''
        if (self._conf.ishaa_zenith is None):
            # ishaa_zenith==None <=> method == Umm al-Qura University, Makkah
            if HijriDate.get_hijri(self._date,
                                  self._correction_val).month == 9:
                ishaa_t = self._dohr_time()
                + self._time(self._conf.maghreb_zenith) + 2.0
            else:
                ishaa_t = self._dohr_time()
                + self._time(self._conf.maghreb_zenith) + 1.5
        else:
            ishaa_t = self._time(self._conf.ishaa_zenith)
            ishaa_t = self._dohr_time() + ishaa_t
        return Prayer._hours_to_time(ishaa_t, shift,
                                           self._conf.summer_time)

