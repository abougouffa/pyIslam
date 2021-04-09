from pyIslam.zakat import Zakat


print("\n---testing zakat---\n")

z = Zakat()
print(str(z.calculate_zakat(10000)) + " $")
print(str(z.calculate_zakat_harvest(10000)) + " Kg")
print(str(z.calculate_zakat_harvest(10000, "natural", "other")) + " Kg")
