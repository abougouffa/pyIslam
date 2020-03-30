# -*- coding: utf-8 -*-

from pyIslam.baselib import dcos, dsin
from math import atan, pi


class Qiblah:
    def __init__(self, conf):
        self._conf = conf
        MAKKAH_LATI = 21.42249   # latitude taken from maps.google.com
        MAKKAH_LONG = 39.826174  # longitude taken from maps.google.com
        lamda = MAKKAH_LONG - self._conf.longitude
        num = dcos(MAKKAH_LATI) * dsin(lamda)
        denom = (dsin(MAKKAH_LATI) * dcos(self._conf.latitude)
                 - dcos(MAKKAH_LATI) * dsin(self._conf.latitude)
                 * dcos(lamda))
        self._qiblah_dir = (180 / pi) * atan(num / denom)
        
        # Needs a check!
        if denom < 0:
            self._qiblah_dir = 180 + self._qiblah_dir
        if denom > 0 and num < 0:
            self._qiblah_dir = 360 + self._qiblah_dir

    def direction(self):
        '''Get the direction from the north of the qiblah (in degrees)'''
        return self._qiblah_dir

    def sixty(self):  # Convert the angle from degrees to sixty
        six = str(int(self._qiblah_dir)) + '°'
        self._qiblah_dir = (self._qiblah_dir - int(self._qiblah_dir)) * 60
        six = six + " " + str(int(self._qiblah_dir)) + "'"
        self._qiblah_dir = (self._qiblah_dir - int(self._qiblah_dir)) * 60
        six = six + " " + str(int(self._qiblah_dir)) + "''"
        self._qiblah_dir = (self._qiblah_dir - int(self._qiblah_dir)) * 60
        return six

