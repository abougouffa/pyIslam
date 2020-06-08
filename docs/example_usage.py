#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyIslam.praytimes import PrayerConf, Prayer, LIST_FAJR_ISHA_METHODS
from pyIslam.hijri import HijriDate
from pyIslam.qiblah import Qiblah
from datetime import date, datetime
from pyIslam.mirath import Mirath
from pyIslam.zakat import Zakat
from pyIslam.baselib import gregorian_to_julian
import pyIslam.baselib_unit_test

# Latitude = 36.716667
# Longitude = 3.250000

print('''Usage example of pyIslam
-------------------------------------''')

ar = ('Shafii, Maliki, Hambali', 'Hanafi')

longitude = input('1. Enter the longitude of your city: ')

if longitude == '':
    print('\nUsing the default values: Country = France, State = Algiers')
    longitude = 0.1123912
    latitude = 45.6186566
    timezone = 2
    fajr_isha_method = 6
    asr_fiqh = 1
else:
    longitude = float(longitude)
    latitude = float(input('2. Enter the latitude of your city: '))
    timezone = float(input('3. Enter the timezone of your country (GMT+n): '))

    print('\n4. Choose the Fajr and Ishaa reference:\n-------------------------------------')

    for method in LIST_FAJR_ISHA_METHODS:
        print('{} = {}'.format(method.id, " | ".join(method.organizations)))

    fajr_isha_method = int(input('Enter your choice (from 1 to 5): '))

    print('\n5. Choose the Asr Madhab:\n-------------------------------------')
    print('1 = {}\n2 = {}'.format(ar[0], ar[1]))
    asr_fiqh = int(input('Enter your choice (1 or 2): '))

pconf = PrayerConf(longitude, latitude, timezone, fajr_isha_method, asr_fiqh)

pt = Prayer(pconf, date.today())
hijri = HijriDate.today()

print('Longitude:\n\t', longitude)
print('Latitude:\n\t', latitude)


def tz(t):
    if t < 0:
        return 'GMT' + str(t)
    else:
        return 'GMT+' + str(t)


print('Timezone:\n\t', tz(timezone))
print('Fajr and Ishaa reference:\n\t',
      LIST_FAJR_ISHA_METHODS[fajr_isha_method - 1].organizations[0])
print('Asr madhab:\n\t', ar[asr_fiqh - 1])
print('\nPrayer times for: ' + hijri.format(2) + ' '
      + str(hijri.to_gregorian()))
print('Fajr      : ' + str(pt.fajr_time()))
print('Sherook   : ' + str(pt.sherook_time()))
print('Dohr      : ' + str(pt.dohr_time()))
print('Asr       : ' + str(pt.asr_time()))
print('Maghreb   : ' + str(pt.maghreb_time()))
print('Ishaa     : ' + str(pt.ishaa_time()))
print('1st third : ' + str(pt.second_third_of_night()))
print('Midnight  : ' + str(pt.midnight()))
print('Qiyam     : ' + str(pt.last_third_of_night()))

print('Qiblah direction from the north: ' + Qiblah(pconf).sixty())

print('\n---testing zakat---\n')

z = Zakat()
print(str(z.calculate_zakat(10000)) + ' $')
print(str(z.calculate_zakat_harvest(10000)) + ' Kg')
print(str(z.calculate_zakat_harvest(10000, 'natural', 'other')) + ' Kg')


print("Julian Day (from datetime.now): {}".format(
    gregorian_to_julian(datetime.now())))

print("Julian Day (from date.today): {}".format(
    gregorian_to_julian(date.today())))


print('\n---Testing Mirath---\n')

test = Mirath()
test.add_relative('wife')
test.add_relative('father')
test.add_relative('maternal_grandmother')
test.add_relative('mother')
test.add_relative('paternal_grandmother')
test.add_relative('sister')
test.add_relative('brother')
test.add_relative('maternal_brother', 3)
test.add_relative('son')
test.calculte_mirath()
# test.display_shares()
