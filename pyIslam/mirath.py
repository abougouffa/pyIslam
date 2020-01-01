# -*- coding: utf-8 -*-

'''
O=============================================================================O
relatives that can't take remain (taasib) : 
    o mother
    o maternal_grandmother
    o paternal_grandmother
    o husband
    o wife
    o maternal_brother
    o maternal_sister

relatives non eligible for inheritance :
    o mother's father
    o aunt
    o sister's son
    o daughter's son
    o daughter's daughter
    o step-family or adopted childrens
    o wife or husband from secret mariage 
    o paternal brother's daugther
    o maternal uncle
    o non-muslim

to do:
    handle invalid user entry
    test further for more corrections
    mention sources of mirath rules
O=============================================================================O
'''
from fractions import Fraction

def get_list_index(liste, element):
    for i in range(len(liste)):
        if liste[i] == element:
            return i
    return -1


class Mirath():

    log = ""

    #the only way i know to initialise empty list of variables of specifique type
    relative_list = [' ']
    relative_list.pop()
    count_list = [0]
    count_list.pop()
    result_list = [Fraction('1/7')]
    result_list.pop()

    def add_relative(self, relative, count = 1):
        self.relative_list.append(relative)
        self.count_list.append(count)
    
    def display_shares(self):
        print('')
        self.log += '\n'
        print('current results :')
        self.log += 'current results :\n'
        for i in range (len(self.result_list)):
            print(str(self.relative_list[i]) + ' -> ' + str(self.result_list[i]))
            self.log += (str(self.relative_list[i]) + ' -> ' + str(self.result_list[i]) + '\n')
    def calculte_mirath(self):
        offspring = ['son', 'daughter','grandson']
        male_offspring = ['son','grandson']
        sibling = ['brother', 'sister','paternal_brother','paternal_sister','maternal_brother','maternal_sister']
        sibling_offspring = ['brother', 'sister','grandson','grandson']
        for i in range(len(self.relative_list)):
            case = self.relative_list[i]
            
            if case == 'wife':
                if self._exist(offspring):
                    self.result_list.append(Fraction('1/8'))
                else:
                    self.result_list.append(Fraction('1/4'))

            if case == 'husband':
                if self._exist(offspring):
                    self.result_list.append(Fraction('1/4'))
                else:
                    self.result_list.append(Fraction('1/2'))

            if case == 'son':
                    self.result_list.append(Fraction('-1/1'))
            
            if case == 'daughter':
                if self._exist(['son']):
                    self.result_list.append(Fraction('-2/1'))
                else:
                    if self.count_list[i] > 1:
                        self.result_list.append(Fraction('2/3'))
                    else:
                        self.result_list.append(Fraction('1/2'))

            if case == 'father':
                if self._exist(['son','grandson']):
                    self.result_list.append(Fraction('1/6'))
                else:
                    self.result_list.append(Fraction('-1/1'))

            if case == 'mother':
                if self._exist(offspring) or self._count_sibling() > 1:
                    self.result_list.append(Fraction('1/6'))
                else:
                    self.result_list.append(Fraction('1/3'))

            if case == 'grandson':
                if self._exist(['son', 'daughter']):
                    self.result_list.append(Fraction('0/3'))
                else:
                    self.result_list.append(Fraction('-1/1'))

            if case == 'granddaughter':
                if self._exist(['son']):
                    self.result_list.append(Fraction('0/1'))
                elif self._exist(['grandson']):
                    self.result_list.append(Fraction('-2/1'))
                else:
                    if self.count_list[i] > 1:
                        self.result_list.append(Fraction('2/3'))
                    else:
                        self.result_list.append(Fraction('1/2'))

            if case == 'grandfather':
                if not self._exist(['father']) and self._exist(['son','grandson']):
                    self.result_list.append(Fraction('1/6'))
                elif not self._exist(['father']):
                    self.result_list.append(Fraction('-1/1'))
                else:
                    self.result_list.append(Fraction('0/1'))

            if case == 'paternal_grandmother':
                if not self._exist(['mother','father','maternal_grandmother']):
                    self.result_list.append(Fraction('1/6'))
                elif not self._exist(['mother','father']) and self._exist(['maternal_grandmother']):
                    self.result_list.append(Fraction('1/12'))
                else:
                    self.result_list.append(Fraction('0/1'))
            
            if case == 'maternal_grandmother':
                if not self._exist(['mother','father','paternal_grandmother']):
                    self.result_list.append(Fraction('1/6'))
                elif not self._exist(['mother']) and self._exist(['maternal_grandmother']):
                    self.result_list.append(Fraction('1/12'))
                else:
                    self.result_list.append(Fraction('0/1'))

            if case == 'brother':
                if self._exist(['son', 'daughter','father']):
                    self.result_list.append(Fraction('0/1'))
                else:
                    self.result_list.append(Fraction('-1/1'))
            
            if case == 'sister':
                if self._exist(['son', 'daughter','father']):
                    self.result_list.append(Fraction('0/1'))
                elif self._exist(['brother']):
                    self.result_list.append(Fraction('-2/1'))
                else:
                    if self.count_list[i] > 1:
                        self.result_list.append(Fraction('2/3'))
                    else:
                        self.result_list.append(Fraction('1/2'))

            if case == 'paternal_brother':
                if (not self._exist(['brother','father'])) and (not self._exist(offspring)):
                    self.result_list.append(Fraction('-1/1'))
                else:
                    self.result_list.append(Fraction('0/2'))


            if case == 'paternal_sister':
                if not self._exist(['brother','grandfather']) and not self._exist(offspring): 
                    if self._exist(['sister']) and not self._exist(['paternal_brother']):
                        j = get_list_index(self.relative_list, 'sister')
                        if self.count_list[j] == 1:
                            self.result_list.append(Fraction('1/6'))
                    elif self._exist(['paternal_brother']):
                            self.result_list.append(Fraction('-2/1'))
                    else:
                        if self.count_list[i] > 1:
                            self.result_list.append(Fraction('2/3'))
                        else:
                            self.result_list.append(Fraction('1/2'))
                else:
                    self.result_list.append(Fraction('0/6'))
            
            if case == 'maternal_brother' or case == 'maternal_sister':
                if self._exist(male_offspring) or self._exist(['father','grandfather']):
                    self.result_list.append(Fraction('0/3'))
                else:
                    if self._count_maternal_sibling() > 1:
                        self.result_list.append(Fraction('1/3'))
                    else:
                        self.result_list.append(Fraction('1/6'))

            if case == 'nephew':
                if self._exist(offspring) or self._exist(['brother','father','grandfather'\
                    ,'paternal_brother','maternal_brother']):
                    self.result_list.append(Fraction('0/1'))
                else:
                    self.result_list.append(Fraction('-1/1'))
            
            if case == 'paternal_nephew':
                if self._exist(offspring) or self._exist(['brother','father','grandfather'\
                    ,'paternal_brother','maternal_brother','nephew']):
                    self.result_list.append(Fraction('0/1'))
                else:
                    self.result_list.append(Fraction('-1/1'))
            
            if case == 'nephew_son':
                if self._exist(offspring) or self._exist(['brother','father','grandfather'\
                    ,'paternal_brother','maternal_brother','nephew','paternal_nephew']):
                    self.result_list.append(Fraction('0/1'))
                else:
                    self.result_list.append(Fraction('-1/1'))
            
            if case == 'paternal_nephew_son':
                if self._exist(offspring) or self._exist(['brother','father','grandfather'\
                    ,'paternal_brother','maternal_brother','nephew','paternal_nephew','nephew_son']):
                    self.result_list.append(Fraction('0/1'))
                else:
                    self.result_list.append(Fraction('-1/1'))
            
            if case == 'paternal_uncle':
                if self._exist(offspring) or self._exist(['brother','father','grandfather',\
                    'paternal_brother','maternal_brother','nephew','paternal_nephew','nephew_son'\
                    ,'paternal_nephew_son']):
                    self.result_list.append(Fraction('0/1'))
                else:
                    self.result_list.append(Fraction('-1/1'))

            if case == 'paternal_paternal_uncle':
                if self._exist(offspring) or self._exist(['brother','father','grandfather'\
                    ,'paternal_brother','maternal_brother','nephew','paternal_nephew','nephew_son'\
                    ,'paternal_nephew_son','paternal_uncle']):
                    self.result_list.append(Fraction('0/1'))
                else:
                    self.result_list.append(Fraction('-1/1'))

            if case == 'cousin':
                if self._exist(offspring) or self._exist(['brother','father','grandfather'\
                    ,'paternal_brother','maternal_brother','nephew','paternal_nephew','nephew_son'\
                    ,'paternal_nephew_son','paternal_uncle','paternal_paternal_uncle']):
                    self.result_list.append(Fraction('0/1'))
                else:
                    self.result_list.append(Fraction('-1/1'))

            if case == 'paternal_cousin':
                if self._exist(offspring) or self._exist(['brother','father','grandfather'\
                    ,'paternal_brother','maternal_brother','nephew','paternal_nephew','nephew_son'\
                    ,'paternal_nephew_son','paternal_uncle','paternal_paternal_uncle','cousin']):
                    self.result_list.append(Fraction('0/1'))
                else:
                    self.result_list.append(Fraction('-1/1'))
            
            if case == 'cousin_son':
                if self._exist(offspring) or self._exist(['brother','father','grandfather'\
                    ,'paternal_brother','maternal_brother','nephew','paternal_nephew','nephew_son'\
                    ,'paternal_nephew_son','paternal_uncle','paternal_paternal_uncle','cousin',\
                    'paternal_cousin']):
                    self.result_list.append(Fraction('0/1'))
                else:
                    self.result_list.append(Fraction('-1/1'))

            if case == 'paternal_cousin_son':
                if self._exist(offspring) or self._exist(['brother','father','grandfather'\
                    ,'paternal_brother','maternal_brother','nephew','paternal_nephew','nephew_son'\
                    ,'paternal_nephew_son','paternal_uncle','paternal_paternal_uncle','cousin'\
                    ,'paternal_cousin','cousin_son']):
                    self.result_list.append(Fraction('0/1'))
                else:
                    self.result_list.append(Fraction('-1/1'))

            if case == 'cousin_grandson':
                if self._exist(offspring) or self._exist(['brother','father','grandfather'\
                    ,'paternal_brother','maternal_brother','nephew','paternal_nephew','nephew_son'\
                    ,'paternal_nephew_son','paternal_uncle','paternal_paternal_uncle','cousin'\
                    ,'paternal_cousin','cousin_son','paternal_cousin_son']):
                    self.result_list.append(Fraction('0/1'))
                else:
                    self.result_list.append(Fraction('-1/1'))

            if case == 'paternal_cousin_grandson':
                if self._exist(offspring) or self._exist(['brother','father','grandfather'\
                    ,'paternal_brother','maternal_brother','nephew','paternal_nephew','nephew_son'\
                    ,'paternal_nephew_son','paternal_uncle','paternal_paternal_uncle','cousin'\
                    ,'paternal_cousin','cousin_son','paternal_cousin_son','cousin_grandson']):
                    self.result_list.append(Fraction('0/1'))
                else:
                    self.result_list.append(Fraction('-1/1'))

        self._correct_ratio()

    def _correct_ratio(self):
        #1-calcute total
        total = Fraction('0/1')
        for i in range (len(self.result_list)):
            if self.result_list[i] > 0:
                total += self.result_list[i]
                print(str(self.relative_list[i]) + ' take ' + str(self.result_list[i]))
                self.log += (str(self.relative_list[i]) + ' take ' + str(self.result_list[i]) + '\n')

        #2-distribuate remains if there is
        isbam = get_list_index(self.result_list, -1)
        isbaf = get_list_index(self.result_list, -2)
        if isbam != -1 and isbaf != -1:
            male = self.count_list[isbam]
            female = self.count_list[isbaf]
            shares = male * 2 + female
            self.result_list[isbam] = (Fraction('1/1') - total) * Fraction(male*2, shares)
            self.result_list[isbaf] = (Fraction('1/1') - total) * Fraction(female, shares)      
            # self.result_list[isbam] = (Fraction('1/1') - total) * Fraction('2/3') * count_list[isbam]
            # self.result_list[isbaf] = (Fraction('1/1') - total) * Fraction('1/3') * count_list[isbam]       
            print(str(self.relative_list[isbam]) + ' and ' + str(self.relative_list[isbaf]) + ' take the remain')
            self.log += (str(self.relative_list[isbam]) + ' and ' + str(self.relative_list[isbaf]) + ' take the remain' + '\n')
            return
        if isbam != -1 and isbaf == -1:
            self.result_list[isbam] = Fraction('1/1') - total
            print(str(self.relative_list[isbam]) + ' take remain')
            self.log += (str(self.relative_list[isbam]) + ' take remain' + '\n')
            return


        #3-equalify the shares if necesary
        den = total.numerator
        num = total.denominator
        if total != 1:
            print('correting total')
            self.log += ('correting total' + '\n')
            total = Fraction(0, 1)
            for i in range (len(self.result_list)):
                self.result_list[i] *= Fraction(num, den)
                total += self.result_list[i]
                print(str(self.relative_list[i]) + ' take ' + str(self.result_list[i]))
                self.log += (str(self.relative_list[i]) + ' take ' + str(self.result_list[i]) + '\n')
        print('total corrected = ' + str(total))
        self.log += ('total corrected = ' + str(total) + '\n')

    def _exist(self, liste):
        for i in range(len(self.relative_list)):
            for j in range(len(liste)):
                if self.relative_list[i] == liste[j]:
                    return True
        return False
        
    def _count_sibling(self):
        counter = 0
        for i in range(len(self.relative_list)):
            l = self.relative_list[i]
            if l == 'brother' or l == 'sister' or l == 'paternal_brother' or l == 'paternal_sister':
                counter += self.count_list[i]
        return counter + self._count_maternal_sibling()

    def _count_maternal_sibling(self):
        counter = 0
        for i in range(len(self.relative_list)):
            l = self.relative_list[i]
            if l == 'maternal_brother' or l == 'maternal_sister':
                counter += self.count_list[i]
        return counter

