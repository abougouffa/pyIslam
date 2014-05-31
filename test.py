#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyIslam.praytimes import *
from pyIslam.hijri import *
from pyIslam.baselib import toSixty
from pyIslam.qiblah import Qiblah
from datetime import date, time


# Latitude = 36.716667
# Longitude = 3.250000

print('''Assalat Imade Eddin 0.1.1 - an islamic prayer times calculator
Written by (Al-Fakir Ila Allah): Abdelhak Mohammed Bougouffa
abdelhak.alg@gmail.com [or] abdelhak@cryptolab.net
-------------------------------------''')
fi = (  'University of Islamic Sciences, Karachi',
		'Muslim World League',
		'Egyptian General Authority of Survey',
		'Umm al-Qura University, Makkah',
		'Islamic Society of North America')

ar = ('Shafii', 'Hanafi')

longitude = input('1. Enter the longitude of your city: ')

if longitude == '':
	print('\nUsing the default values: Country = Algeria, State = Algiers')
	longitude = 3.250000
	latitude = 36.716667
	timezone = 1
	fajr_isha_method = 3
	asr_fiqh = 1
else:
	latitude = float(input('2. Enter the latitude of your city: '))
	timezone = float(input('3. Enter the timezone of your country (GMT+n): '))

	print('\n4. Choose the Fajr and Ishaa reference:\n-------------------------------------')
	for j in range(0,5):
		print('%d = %s' %(j,fi[j]))

	fajr_isha_method = int(input('Enter your choice (from 1 to 5): '))

	print('\n5. Choose the Asr Madhab:\n-------------------------------------')
	print('1 = Shafii\n2 = Hanafi')
	asr_fiqh = int(input('Enter your choice (1 or 2): '))

pconf=PrayerConf(float(longitude), latitude, timezone, fajr_isha_method, asr_fiqh, False)
pt = Prayer(pconf, date.today())

hijri = HijriDate.today(1)

print('Longitude:\n\t', longitude)
print('Latitude:\n\t', latitude)
def tz(t):
	if t < 0: return 'GMT' + str(t)
	else: return 'GMT+' + str(t)
print('Timezone:\n\t', tz(timezone))
print('Fajr and Ishaa reference:\n\t', fi[fajr_isha_method - 1])
print('Asr madhab:\n\t', ar[asr_fiqh - 1])

print('\nPrayer times for: ' + hijri.format(2) + ' ' + str(hijri.toGregorian()))
print('Fajr:    ' + str(valToTime(pt.fajrTime())))
print('Sherook: ' + str(valToTime(pt.sherookTime())))
print('Dohr:    ' + str(valToTime(pt.dohrTime())))
print('Asr:     ' + str(valToTime(pt.asrTime())))
print('Maghreb: ' + str(valToTime(pt.maghrebTime())))
print('Ishaa:   ' + str(valToTime(pt.ishaaTime())))

print('Qiblah direction from the north: ' + toSixty(Qiblah(pconf).direction()))
