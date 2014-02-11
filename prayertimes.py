#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Prayer Times is a free islamic prayer times calculator
Copyright © 2010 Abdelhak Mohammed Bougouffa (abdelhak.alg@gmail.com)

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

from math import *
from datetime import date, time
from baselib import *
from hijriorganizer import *


def to_sixty(deg): # Convert an angle from degree to sixty
	six = str(int(deg)) + 'degree'
	deg = (deg - int(deg)) * 60
	six = six + " " + str(int(deg)) + "'"
	deg = (deg - int(deg)) * 60
	six = six + " " + str(int(deg)) + "''"
	deg = (deg - int(deg)) * 60
	return six


def val_to_time(val, summer_time = False): # Convert a decimal value (in hours) to time object
	if summer_time == True: st = 1
	else: st = 0
	hour = val
	minute = (hour - int(hour)) * 60
	second = (minute - int(minute)) * 60
	return time((int(hour) + st), int(minute), int(second))


class prayertimes: # Prayer times calculating class
    longitude = 0
    latitude = 0
    timezone = 0
    summer_time = 0
    asr_religion = 1
    fajr_zenith = 108
    sherook_zenith = 90.83333
    maghreb_zenith = 90.83333
    isha_zenith = 108
    date = 0
    middle_longitude = 0
    longitude_diference = 0
    other_infos = list()


    def __init__(self, longitude, latitude, timezone, fajr_isha_method, asr_relig, dat, enable_summer_time): # Constructor
        self.longitude = longitude
        self.latitude = latitude
        self.timezone = timezone

        if (asr_relig == 1 or asr_relig == 2):
            self.asr_religion = asr_relig # 1 = Shafii (Default), 2 = Hanafi
        else: self.asr_religion = 1

        self.date = dat
        self.middle_longitude = self.timezone * 15
        self.longitude_diference = (self.middle_longitude - self.longitude) / 15
        

        if (enable_summer_time == True):
            self._summer_time = 1
        else:
            self._summer_time = 0

        if (fajr_isha_method == 1):   # 1 = University of Islamic Sciences, Karachi
            self.fajr_zenith = 108.0     # 90 + 18.0
            self.isha_zenith = 108.0     # 90 + 18.0
        elif (fajr_isha_method == 2): # 2 = World Islamic League
            self.fajr_zenith = 108.0     # 90 + 18.0
            self.isha_zenith = 107.0     # 90 + 17.0
        elif (fajr_isha_method == 3): # 3 = Egiptian General Organization of Surveying
            self.fajr_zenith = 109.5     # 90 + 19.5
            self.isha_zenith = 107.5     # 90 + 17.5
        elif (fajr_isha_method == 4): # 4 = Um Al-Qura Committee
            self.fajr_zenith = 108.5     # 90 + 18.5
            self.isha_zenith = 0.0       # 90 minutes after the maghreb time (or 120 minutes in Ramadan only)
        elif (fajr_isha_method == 5): # 5 = Islamic Society of North America
            self.fajr_zenith = 105.0     # 90 + 15.0
            self.isha_zenith = 105.0     # 90 + 15.0


    def equation_of_time(self): # Get equation of time
        n = gregorian_to_julian_day(self.date) - 2451544.5
        g = 357.528 + 0.9856003 * n
        c = 1.9148 * dsin(g) + 0.02 * dsin(2 * g) + 0.0003 * dsin(3 * g)
        lamda = 280.47 + 0.9856003 * n + c
        r = -2.468 * dsin(2 * lamda) + 0.053 * dsin(4 * lamda) + 0.0014 * dsin(6 * lamda)
        return (c + r) * 4


    def asr_zenith(self): # Get the zenith angle for asr pray (according to choosed asr religion)
        delta = self.sun_declination()
        x = dsin(self.latitude) * dsin(delta) + dcos(self.latitude) * dcos(delta)
        a = atan(x / sqrt(-x * x + 1))
        x = self.asr_religion + (1 / tan(a))
        return (90 - (180 / pi) * (atan(x) + 2 * atan(1)))


    def sun_declination(self): # Get sun declination
        n = gregorian_to_julian_day(self.date) - 2451544.5
        epsilon = 23.44 - 0.0000004 * n
        l = 280.466 + 0.9856474 * n
        g = 357.528 + 0.9856003 * n
        lamda = l + 1.915 * dsin(g) + 0.02 * dsin(2 * g)
        x = dsin(epsilon) * dsin(lamda)
        return (180 / (4 * atan(1))) * atan(x / sqrt(-x * x + 1))


    def other_informations(self):
        n = gregorian_to_julian_day(self.date) - 2451545.0
        epsilon = 23.440 - 0.0000004 * n # Obliquity of ecliptic (in degree)
        self.other_infos.append(epsilon)

        l = 280.466 + 0.9856474 * n # Mean longitude of Sun, corrected for aberration (in degree)
        self.other_infos.append(l)
       
        g = 357.528 + 0.9856003 * n # Mean Anomaly (in degree)
        self.other_infos.append(g)

        while (l < 0): l = l + 360
        while (l > 360): l = l - 360
        while (g < 0): g = g + 360
        while (g > 360): g = g - 360

        lamda = l + 1.915 * dsin(g) + 0.020 * dsin(2 * g) # Ecliptic longitude (in degree)
        self.other_infos.append(lamda)

        dist = 1.00014 - 0.01671 * dcos(g) - 0.00014 * dcos(2 * g) # Distruption between the sun and earth
        self.other_infos.append(dist * 150000000) # Distruption between the sun and earth converted to KiloMetre
        
        sd = 0.2666 / dist # Semi diameter (in degree)
        self.other_infos.append(sd)


    def fajr_time(self): # Fajr Time
        return self.duhr_time() - self.prayer_time(self.fajr_zenith)


    def sherook_time(self): # Sherook Time
        return self.duhr_time() - self.prayer_time(self.sherook_zenith)


    def duhr_time(self): # Duhr Time
        ld = self.longitude_diference
        time_eq = self.equation_of_time()
        duhr_t = 12 + ld + time_eq / 60
        return duhr_t
        return h


    def asr_time(self): # Asr Time
        return self.duhr_time() + self.prayer_time(self.asr_zenith())


    def maghreb_time(self): # Maghreb Time
        return self.duhr_time() + self.prayer_time(self.maghreb_zenith)


    def isha_time(self): # Isha Time
        if (self.isha_zenith == 0.0):
            hij = today(1)
            if (hij.month == 9):
                isha_t = self.maghreb_time() + 2.0 # 2.0 hours = 120 minutes
            else:
                isha_t = self.maghreb_time() + 1.5 # 1.5 hours = 90 minutes
        else:
            isha_t = self.prayer_time(self.isha_zenith)
            isha_t = self.duhr_time() + isha_t
        return isha_t


    def prayer_time(self, zenith): # Get Times for "Fajr, Sherook, Asr, Maghreb, Isha"
        delta = self.sun_declination()
        s = (dcos(zenith) - dsin(self.latitude) * dsin(delta)) / (dcos(self.latitude) * dcos(delta))
        return ((180 / pi * (atan(-s / sqrt(-s * s + 1)) + pi / 2)) / 15)


    def qubla_direction(self): # Get the direction of qubla (El-Masjid al-haram - Makkah) - in degree
        makkah_latitude = 21.4233 #21.433332
        makkah_longitude = 39.8233 #39.766666
        lamda = makkah_longitude - self.longitude
        numerator = dcos(makkah_latitude) * dsin(lamda)
        denominator = dsin(makkah_latitude) * dcos(self.latitude) - dcos(makkah_latitude) * dsin(self.latitude) * dcos(lamda)
        qubla_dir = (180 / pi) * atan(numerator / denominator)
        if (numerator > 0 and denominator < 0): qubla_dir = 180 + qubla_dir
        if (numerator < 0 and denominator < 0): qubla_dir = 180 + qubla_dir
        if (numerator < 0 and denominator > 0): qubla_dir = 360 + qubla_dir
        return qubla_dir





