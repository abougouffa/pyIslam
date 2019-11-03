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

    def calculate_zakat(self, amount) :
        #minimal amount is 4000 dollars approximatively this days
        nisab = 4000 
        if amount <= nisab:
            return 0
        result = amount / 10 / 4
        return result   

    def calculate_zakat_harvest(self, weight, irrigationType = 'artificial', method = 'hanafi') :
        #minimal weight in kilogramme
        nisab = 975
        if method == 'hanafi' :
            nisab =  975
        elif method == 'other' :
            nisab = 612
        else :
            print('invalid methode')
            return
            
        if weight <= nisab:
            return 0

        if irrigationType == 'artificial':
            result = weight / 20
            return result   
        elif irrigationType == 'natural':
            result = weight / 10
            return result   
        else :
            print('invalid type of irrigation')
            return

