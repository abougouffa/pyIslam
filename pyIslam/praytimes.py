# -*- coding: utf-8 -*-

from math import pi, atan, sqrt, tan, floor
from datetime import time
from pyIslam.hijri import HijriDate
from pyIslam.baselib import dcos, dsin, gregorian_to_julian
from math import *


class FixedTime():
    def __init__(self, all_year_time_min, ramadan_time_min):
        self._all_year_time = all_year_time_min
        self._ramadan_time = ramadan_time_min

    @property
    def ramadan_time_hr(self):
        return self._ramadan_time / 60.0

    @property
    def all_year_time_hr(self):
        return self._all_year_time / 60.0


class MethodInfo:
    def __init__(self, method_id, organizations, fajr_angle, ishaa_angle, applicability=()):
        self._id = method_id
        self._organizations = organizations if type(
            organizations) in (list, tuple) else (organizations,)
        self._fajr_angle = fajr_angle
        self._ishaa_angle = ishaa_angle
        self._applicability = applicability if type(
            applicability) in (list, tuple) else (applicability,)

    @property
    def id(self):
        return self._id

    @property
    def organizations(self):
        return self._organizations

    @property
    def fajr_angle(self):
        return self._fajr_angle

    @property
    def ishaa_angle(self):
        return self._ishaa_angle

    @property
    def applicability(self):
        return self._applicability


LIST_FAJR_ISHA_METHODS = (
    MethodInfo(1, ("University of Islamic Sciences, Karachi (UISK)",
                   "Ministry of Religious Affaires, Tunisia",
                   "France - Angle 18°"),
               18.0, 18.0, ()),

    MethodInfo(2, ("Muslim World League (MWL)",
                   "Ministry of Religious Affaires and Awqaf, Algeria",
                   "Presidency of Religious Affairs, Turkey"),
               18.0, 17.0, ()),

    MethodInfo(3, "Egyptian General Authority of Survey (EGAS)",
               19.5, 17.5, ()),

    MethodInfo(4, "Umm al-Qura University, Makkah (UMU)",
               18.5, FixedTime(90, 120), ()),

    MethodInfo(5, ("Islamic Society of North America (ISNA)",
                   "France - Angle 15°"),
               15.0, 15.0, ()),

    MethodInfo(6, "French Muslims (ex-UOIF)",
               12.0, 12.0, ()),

    MethodInfo(7, ("Islamic Religious Council of Signapore (MUIS)",
                   "Department of Islamic Advancements of Malaysia (JAKIM)",
                   "Ministry of Religious Affairs of Indonesia (KEMENAG)"),
               20.0, 18.0, ()),

    MethodInfo(8, "Spiritual Administration of Muslims of Russia",
               16.0, 15.0, ()),

    MethodInfo(9, "Fixed Ishaa Time Interval, 90min",
               19.5, FixedTime(90, 90), ()),

)


class PrayerConf:
    def __init__(self, longitude, latitude, timezone, angle_ref=3,
                 asr_madhab=1, enable_summer_time=False):
        '''Initialize the PrayerConf object
        @param longitude: geographical longitude of the given location
        @param latitude: geographical latitude of the given location
        @param timezone: the time zone GMT(+/-timezone)
        @param angle_ref: integer value for the Fajr and Ishaa angle angle reference
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

        global LIST_FAJR_ISHA_METHODS

        method = LIST_FAJR_ISHA_METHODS[angle_ref - 1] if angle_ref <= len(
            LIST_FAJR_ISHA_METHODS) else LIST_FAJR_ISHA_METHODS[2]

        # Pythonista way to write switch-case instruction
        self.fajr_angle = (method.fajr_angle +
                           90.0) if type(method.fajr_angle) is not FixedTime else method.fajr_angle
        self.ishaa_angle = (method.ishaa_angle +
                            90.0) if type(method.ishaa_angle) is not FixedTime else method.ishaa_angle


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
        return Prayer._hours_to_time(self._dohr_time()
                                     - self._time(self._conf.sherook_angle),
                                     shift, self._conf.summer_time)

    def dohr_time(self, shift=0.0):
        return Prayer._hours_to_time(self._dohr_time(),
                                     shift, self._conf.summer_time)

    def asr_time(self, shift=0.0):
        '''Get the Asr time'''
        return Prayer._hours_to_time(self._dohr_time() + self._time(self._asr_angle()),
                                     shift, self._conf.summer_time)

    def maghreb_time(self, shift=0.0):
        '''Get the Maghreb time'''
        return Prayer._hours_to_time(self._dohr_time() + self._time
                                     (self._conf.maghreb_angle), shift, self._conf.summer_time)

    def ishaa_time(self, shift=0.0):
        '''Get the Ishaa time'''
        if (type(self._conf.ishaa_angle) is FixedTime):
            is_ramadan = HijriDate.get_hijri(
                self._date, self._correction_val).month == 9

            time_after_maghreb = self._conf.ishaa_angle.ramadan_time_hr if is_ramadan else self._conf.ishaa_angle.all_year_time_hr

            ishaa_t = (time_after_maghreb + self._dohr_time() +
                       self._time(self._conf.maghreb_angle))
        else:
            ishaa_t = self._dohr_time() + self._time(self._conf.ishaa_angle)
        return Prayer._hours_to_time(ishaa_t, shift,
                                     self._conf.summer_time)
