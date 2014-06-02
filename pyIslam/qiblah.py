# -*- coding: utf-8 -*-

from pyIslam.baselib import dcos, dsin
from math import atan, pi


class Qiblah():
    def __init__(self, conf):
        self.__conf = conf
        MAKKAH_LATI = 21.42249   # latitude taken from maps.google.com
        MAKKAH_LONG = 39.826174  # longitude taken from maps.google.com
        lamda = MAKKAH_LONG - self.__conf.longitude
        num = dcos(MAKKAH_LATI) * dsin(lamda)
        denom = (dsin(MAKKAH_LATI) * dcos(self.__conf.latitude)
                 - dcos(MAKKAH_LATI) * dsin(self.__conf.latitude)
                 * dcos(lamda))
        self.__qiblah_dir = (180 / pi) * atan(num / denom)
        if num > 0 and denom < 0:
            self.__qiblah_dir = 180 + self.__qiblah_dir
        if num < 0 and denom < 0:
            self.__qiblah_dir = 180 + self.__qiblah_dir
        if num < 0 and denom > 0:
            self.__qiblah_dir = 360 + self.__qiblah_dir

    def direction(self):
        '''Get the direction from the north of the qiblah (in degrees)'''
        return self.__qiblah_dir

    def sixty(self):  # Convert an angle from self.__qiblah_dirree to sixty
        six = str(int(self.__qiblah_dir)) + '°'
        self.__qiblah_dir = (self.__qiblah_dir - int(self.__qiblah_dir)) * 60
        six = six + " " + str(int(self.__qiblah_dir)) + "'"
        self.__qiblah_dir = (self.__qiblah_dir - int(self.__qiblah_dir)) * 60
        six = six + " " + str(int(self.__qiblah_dir)) + "''"
        self.__qiblah_dir = (self.__qiblah_dir - int(self.__qiblah_dir)) * 60
        return six
