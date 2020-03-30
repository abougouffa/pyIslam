# -*- coding: utf-8 -*-

'''
O=============================================================================O
#awsoq jam' wisq  = 195 kg hanafi wa 122.4 kg jomhor
#nisab 5 awsoq tomor
#mitkal dahab = 5 gramme
#nisab fida = 595 gr
#nisab dahab = 85 gr
O=============================================================================O
'''
class Zakat():
    def calculate_zakat(self, amount, nisab=4000) :
        #minimal amount is 4000 dollars approximatively this days
        if amount < nisab: # ( < or <= ?! )
            return 0
        return amount * 0.025 # (4th of 10th)   

    def calculate_zakat_harvest(self, weight, irrigationType='artificial', method='hanafi') :
        #minimal weight in kilogramme
        nisab = 975 if method == 'hanafi' else 612

        if weight <= nisab:
            return 0

        if irrigationType == 'artificial':
            return weight * 0.05
        elif irrigationType == 'natural':
            return weight * 0.1
        else:
            raise ValueError("Invalid type of irrigation, it can be one of ['natural', 'artificial']")
            
