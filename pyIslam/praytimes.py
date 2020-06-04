# -*- coding: utf-8 -*-

from math import pi, atan, sqrt, tan, floor
from datetime import time
from pyIslam.hijri import HijriDate
from pyIslam.baselib import dcos, dsin, gregorian_to_julian
from math import *

fajr_isha_angles = \
    {
        1: (108.0, 108.0),  # 1 = University of Islamic Sciences, Karachi
        2: (108.0, 107.0),  # 2 = Muslim World League
        3: (109.5, 107.5),  # 3 = Egyptian General Authority of Survey
        4: (108.5, None),  # 4 = Umm al-Qura University, Makkah
        5: (105.0, 105.0),  # 5 = Islamic Society of North America
        6: (102.0, 102.0),  # 6 = Union of Islamic Organizations of France
        7: (110.0, 108.0)  # 7 = Islamic Religious Council of Signapore
    }

FAJR_ISHA_METHODS = dict(zip(fajr_isha_angles.keys(),
                             ["University of Islamic Sciences, Karachi",
                              "Muslim World League",
                              "Egyptian General Authority of Survey",
                              "Umm al-Qura University, Makkah",
                              "Islamic Society of North America",
                              "Union of Islamic Organizations of France",
                              "Islamic Religious Council of Signapore"]))


class PrayerConf:
    def __init__(self, longitude, latitude, timezone, angle_ref=3,
                 asr_madhab=1, enable_summer_time=False):
        '''Initialize the PrayerConf object
        @param longitude: geographical longitude of the given location
        @param latitude: geographical latitude of the given location
        @param timezone: the time zone GMT(+/-timezone)
        @param angle_ref: integer value for the Fajr and
        Ishaa angle angle reference
        1 = University of Islamic Sciences, Karachi
        2 = Muslim World League
        3 = Egyptian General Authority of Survey (default)
        4 = Umm al-Qura University, Makkah
        5 = Islamic Society of North America
        @param asr_madhab: integer value
        1 = Shafii, Maliki, Hambali (default)
        2 = Hanafi
        @param: enable_summer_time: True if summer time is used in the place,
        False (default) if not'''

        self.longitude = longitude
        self.latitude = latitude
        self.timezone = timezone
        self.sherook_angle = 90.83333  # Constants
        self.maghreb_angle = 90.83333

        if asr_madhab == 2:
            self.asr_madhab = asr_madhab  # 1 = Shafii/Maliki/Hambali, 2 = Hanafi
        else:
            self.asr_madhab = 1

        self.middle_longitude = self.timezone * 15
        self.longitude_difference = (
            self.middle_longitude - self.longitude) / 15

        self.summer_time = enable_summer_time

        global fajr_isha_angles

        # Pythonista way to write switch-case instruction
        (self.fajr_angle, self.ishaa_angle) = fajr_isha_angles.get(
            angle_ref, fajr_isha_angles[3])


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

    def _asr_angle(self):
        '''Get the angle angle for asr (according to choosed asr fiqh)'''
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

    def _dohr_time(self):
        '''# Dohr time for internal use, return number of hours,
        not time object'''
        ld = self._conf.longitude_difference
        time_eq = self._equation_of_time()
        duhr_t = 12 + ld + time_eq / 60
        return duhr_t

    def _time(self, angle):
        '''Get Times for "Fajr, Sherook, Asr, Maghreb, ishaa"'''
        delta = self._sun_declination()
        s = ((dcos(angle)
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
                (self._dohr_time() - self._time(self._conf.fajr_angle),
                 shift, self._conf.summer_time))

    def sherook_time(self, shift=0.0):
        '''Get the Sunrise (Sherook) time'''
        return (Prayer._hours_to_time
                (self._dohr_time()
                 - self._time(self._conf.sherook_angle),
                 shift, self._conf.summer_time))

    def dohr_time(self, shift=0.0):
        return Prayer._hours_to_time(self._dohr_time(),
                                     shift, self._conf.summer_time)

    def asr_time(self, shift=0.0):
        '''Get the Asr time'''
        return (Prayer._hours_to_time
                (self._dohr_time() + self._time(self._asr_angle()),
                 shift, self._conf.summer_time))

    def maghreb_time(self, shift=0.0):
        '''Get the Maghreb time'''
        return (Prayer._hours_to_time
                (self._dohr_time() + self._time
                 (self._conf.maghreb_angle), shift, self._conf.summer_time))

    def ishaa_time(self, shift=0.0):
        '''Get the Ishaa time'''
        if (self._conf.ishaa_angle is None):
            # Assumes ishaa_angle==None <=> method == Umm al-Qura University, Makkah
            if HijriDate.get_hijri(self._date,
                                   self._correction_val).month == 9:
                ishaa_t = self._dohr_time()
                + self._time(self._conf.maghreb_angle) + 2.0
            else:
                ishaa_t = self._dohr_time()
                + self._time(self._conf.maghreb_angle) + 1.5
        else:
            ishaa_t = self._time(self._conf.ishaa_angle)
            ishaa_t = self._dohr_time() + ishaa_t
        return Prayer._hours_to_time(ishaa_t, shift,
                                     self._conf.summer_time)
