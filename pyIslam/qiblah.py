# -*- coding: utf-8 -*-

from pyIslam.baselib import *
from pyIslam.praytimes import PrayerConf
from math import atan

class Qiblah():
    def __init__(self, conf):
        self.__conf=conf

    def direction(self): # Get the direction of qiblah (El-Masjid al-haram - Makkah) - in degree
        MAKKAH_LATI = 21.42249		# Longitude and latitude taken from maps.google.com
        MAKKAH_LONG = 39.826174
        lamda = MAKKAH_LONG - self.__conf.longitude
        nomin = dcos(MAKKAH_LATI) * dsin(lamda)
        denom = dsin(MAKKAH_LATI) * dcos(self.__conf.latitude) - dcos(MAKKAH_LATI) * dsin(self.__conf.latitude) * dcos(lamda)
        qiblah_dir = (180 / pi) * atan(nomin / denom)
        if nomin > 0 and denom < 0: qiblah_dir = 180 + qiblah_dir
        if nomin < 0 and denom < 0: qiblah_dir = 180 + qiblah_dir
        if nomin < 0 and denom > 0: qiblah_dir = 360 + qiblah_dir
        return qiblah_dir
