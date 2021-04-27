from datetime import date

from pyIslam.praytimes import (
    PrayerConf,
    Prayer,
    LIST_FAJR_ISHA_METHODS,
)
from pyIslam.hijri import HijriDate
from pyIslam.qiblah import Qiblah


print(
    """Usage example of pyIslam
-------------------------------------"""
)

ar = ("Shafii, Maliki, Hambali", "Hanafi")

longitude = input("1. Enter the longitude of your city: ")

if longitude == "":
    print("\nUsing the default values: Country = France, State = Angouleme")
    longitude = 0.1099341
    latitude = 45.6458156
    timezone = 2
    fajr_isha_method = 6
    asr_fiqh = 1
else:
    longitude = float(longitude)
    latitude = float(input("2. Enter the latitude of your city: "))
    timezone = float(input("3. Enter the timezone of your country (GMT+n): "))

    print(
        "\n4. Choose the Fajr and Ishaa reference:\n-------------------------------------"
    )

    for method in LIST_FAJR_ISHA_METHODS:
        print("{} = {}".format(method.id, " | ".join(method.organizations)))

    fajr_isha_method = int(input("Enter your choice (from 1 to 5): "))

    # Now you can also define a custom method, based on angle
    # fajr_isha_method = MethodInfo(9, "Custom", 16.5, 16.5)
    # Or fixed time (usually for Ishaa)
    # fajr_isha_method = MethodInfo(9, "Custom", 16.5, FixedTime(90)) # Adds 90 minutes after Maghreb

    print("\n5. Choose the Asr Madhab:\n-------------------------------------")
    print("1 = {}\n2 = {}".format(ar[0], ar[1]))
    asr_fiqh = int(input("Enter your choice (1 or 2): "))

pconf = PrayerConf(longitude, latitude, timezone, fajr_isha_method, asr_fiqh)

pt = Prayer(pconf, date.today())
hijri = HijriDate.today()

print("Longitude:\n\t", longitude)
print("Latitude:\n\t", latitude)


def tz(t):
    if t < 0:
        return "GMT" + str(t)
    else:
        return "GMT+" + str(t)


print("Timezone:\n\t", tz(timezone))
print(
    "Fajr and Ishaa reference:\n\t",
    LIST_FAJR_ISHA_METHODS[fajr_isha_method - 1].organizations[0],
)
print("Asr madhab:\n\t", ar[asr_fiqh - 1])
print("\nPrayer times for: " + hijri.format(2) + " " + str(hijri.to_gregorian()))
print("Fajr      : " + str(pt.fajr_time()))
print("Sherook   : " + str(pt.sherook_time()))
print("Dohr      : " + str(pt.dohr_time()))
print("Asr       : " + str(pt.asr_time()))
print("Maghreb   : " + str(pt.maghreb_time()))
print("Ishaa     : " + str(pt.ishaa_time()))
print("1st third : " + str(pt.second_third_of_night()))
print("Midnight  : " + str(pt.midnight()))
print("Qiyam     : " + str(pt.last_third_of_night()))

print("Qiblah direction from the north: " + Qiblah(pconf).sixty())
