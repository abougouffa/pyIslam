# -*- coding: utf-8 -*-

from datetime import date

from pyIslam.praytimes import (
    PrayerConf,
    Prayer,
)


def test_praytimes_jakarta():
    # tested against https://www.jadwalsholat.org/
    # and the result is extremely accurate

    # https://www.mapcoordinates.net/en
    # jakarta
    latitude = -6.18233995
    longitude = 106.84287154
    timezone = 7  # GMT+7
    fajr_isha_method = 7  # Ministry of Religious Affairs of Indonesia (KEMENAG)
    asr_fiqh = 1  # Jomhor
    prayer_conf = PrayerConf(longitude, latitude, timezone, fajr_isha_method, asr_fiqh)
    prayer_time = Prayer(prayer_conf, date(2021, 4, 9))

    assert str(prayer_time.fajr_time()) == "04:36:34"
    assert str(prayer_time.sherook_time()) == "05:54:14"
    assert str(prayer_time.dohr_time()) == "11:54:14"
    assert str(prayer_time.asr_time()) == "15:12:14"
    assert str(prayer_time.maghreb_time()) == "17:54:14"
    assert str(prayer_time.ishaa_time()) == "19:03:49"
    assert str(prayer_time.second_third_of_night()) == "21:28:21"  # 1 st third
    assert str(prayer_time.midnight()) == "23:15:24"  # midnight
    assert str(prayer_time.last_third_of_night()) == "01:02:28"  # qiyam


def test_praytimes_jakarta_umm_alqura():
    # jakarta
    latitude = -6.18233995
    longitude = 106.84287154
    timezone = 7  # GMT+7
    fajr_isha_method = 4  # Umm al-Qura University, Makkah (UMU)
    asr_fiqh = 1  # Jomhor
    prayer_conf = PrayerConf(longitude, latitude, timezone, fajr_isha_method, asr_fiqh)
    prayer_time = Prayer(prayer_conf, date(2021, 4, 9))

    # other pryer times are same as the test above
    assert str(prayer_time.fajr_time()) == "04:42:39"
    assert str(prayer_time.ishaa_time()) == "19:24:14"
    assert str(prayer_time.second_third_of_night()) == "21:30:22"  # 1 st third
    assert str(prayer_time.midnight()) == "23:18:26"  # midnight
    assert str(prayer_time.last_third_of_night()) == "01:06:30"  # qiyam


def test_praytimes_jakarta_fixed_interval():
    # jakarta
    latitude = -6.18233995
    longitude = 106.84287154
    timezone = 7  # GMT+7
    fajr_isha_method = 9  # "Fixed Ishaa Time Interval, 90min",
    asr_fiqh = 1  # Jomhor
    prayer_conf = PrayerConf(longitude, latitude, timezone, fajr_isha_method, asr_fiqh)
    prayer_time = Prayer(prayer_conf, date(2021, 4, 9))

    # other pryer times are same as the test above
    assert str(prayer_time.fajr_time()) == "04:38:36"
    assert str(prayer_time.ishaa_time()) == "19:24:14"
    assert str(prayer_time.second_third_of_night()) == "21:29:01"  # 1 st third
    assert str(prayer_time.midnight()) == "23:16:25"  # midnight
    assert str(prayer_time.last_third_of_night()) == "01:03:49"  # qiyam
