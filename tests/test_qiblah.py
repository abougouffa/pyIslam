# -*- coding: utf-8 -*-

from pyIslam.praytimes import PrayerConf
from pyIslam.qiblah import Qiblah


def test_qiblah_jakarta():
    # https://www.mapcoordinates.net/en
    # jakarta
    latitude = -6.18233995
    longitude = 106.84287154
    timezone = 7  # GMT+7
    fajr_isha_method = 3  # University of Islamic Sciences, Karachi (UISK)
    asr_fiqh = 1  # Jomhor
    prayer_conf = PrayerConf(longitude, latitude, timezone, fajr_isha_method, asr_fiqh)

    assert Qiblah(prayer_conf).sixty() == "295° 8' 39''"
