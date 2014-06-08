#!/usr/bin/python3

import sys
sys.path.append('../')
from pyIslam.hijri import HijriDate


year = 1
hi = HijriDate(year, 1, 1)
days = [[]]

while hi.year < 1435:
    next_hi = hi.nextDate()
    if next_hi.year != hi.year:
        days.append([])

    if next_hi.isLast():
        days[next_hi.year - year].append \
        ('%04d-%02d = %d' % (next_hi.year, next_hi.month, next_hi.day))

    del hi
    hi = next_hi

for day in days:
    print(day)
