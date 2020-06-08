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
	o uncle from mother (mother's brother) not
	maternal-paternal uncle (father's maternal brother)
	o non-muslim

to do:
	handle invalid user entry
	test further for more corrections
	mention sources of mirath rules
O=============================================================================O
'''
from fractions import Fraction

'''
global function
tell the index of given element in given list
return the index of element in list
return -1 if the list don't contain the element
'''

def get_element_index(liste, element):
	for i in range(len(liste)):
		if liste[i] == element:
			return i
	return -1


class Mirath():

	def __init__(self, name= "new case"):
		self.relative_list = []
		self.count_list = []
		self.result_list = []
		self.log = []
		self.name = name

	def _append_to_log(self, text):
		self.log.append(str(text + '\n'))
		#print(text)
	def display_log(self):
		log = self.log
		print('\n++++++++++++++++++++++ ' + self.name + ' ++++++++++++++++++++++++++++\n')
		for line in log :
			line = line[:-1]
			print(line)
		print('\n+++++++++++++++++++++++ end +++++++++++++++++++++++++++++\n')

	
	def add_relative(self, relative, count = 1):
		self.relative_list.append(relative)
		self.count_list.append(count)
	
	# def display_shares(self):
	#   self._append_to_log('current results :')
	#   for i in range(len(self.result_list)):
	#       self._append_to_log(str(self.relative_list[i]) + ' -> ' + str(self.result_list[i]))
	
	def calculate_mirath(self):
		females = ['son', 'grandson']
		males = ['son', 'grandson', 'father', 'grandfather', 'paternal_brother', 'maternal_brother', 'brother', 'uncle', 'cousin', 'paternal_uncle', 'paternal_cousin']

		ancestor = ['father', 'grandfather', 'mother', 'maternal_grandmother', 'paternal_grandmother']
		male_ancestor = ['father', 'grandfather']
		female_ancestor = ['mother', 'maternal_grandmother', 'paternal_grandmother']

		offspring = ['son', 'daughter', 'grandson', 'granddaughter']
		male_offspring = ['son', 'grandson']
		female_offspring = ['daughter', 'granddaughter']
		
		sibling = ['brother', 'sister', 'paternal_brother', 'paternal_sister', 'maternal_brother', 'maternal_sister']
		males_sibling = ['son', 'grandson']
		female_sibling = ['son', 'grandson']
		paternal_sibling = ['paternal_brother', 'paternal_sister']
		maternal_sibling = ['maternal_brother', 'maternal_sister']
		
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
				if self._exist(offspring):
					self.result_list.append(Fraction('1/6'))
				else:
					self.result_list.append(Fraction('-1/1'))

			if case == 'mother':
				if self._exist(offspring) or self._count_sibling() > 1:
					self.result_list.append(Fraction('1/6'))
				elif self._exist(['father']) and not self._exist(offspring):
					self.result_list.append(Fraction('-2/1'))
				else:
					self.result_list.append(Fraction('1/3'))

			if case == 'paternal_maternal_uncle':
				if self._exist(offspring) or self._count_sibling() > 1:
					self.result_list.append(Fraction('1/6'))
				elif self._exist(['father']):
					self.result_list.append(Fraction('0/1'))
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
				elif self._exist(['daughter']) and not self._exist(['grandson', 'son']):
					daughter_idx = get_element_index(self.relative_list, 'daughter')
					if self.count_list[daughter_idx] == 1:
						self.result_list.append(Fraction('1/6'))
					else:
						self.result_list.append(Fraction('0/1'))
				elif self._exist(['grandson']):
					self.result_list.append(Fraction('-2/1'))
				else:
					if self.count_list[i] > 1:
						self.result_list.append(Fraction('2/3'))
					else:
						self.result_list.append(Fraction('1/2'))

			if case == 'grandfather':
				if not self._exist(['father']) and self._exist(offspring):
					self.result_list.append(Fraction('1/6'))
				elif not self._exist(['father']):
					self.result_list.append(Fraction('-1/1'))
				else:
					self.result_list.append(Fraction('0/1'))

			if case == 'paternal_grandmother':
				if not self._exist(['mother', 'father', 'maternal_grandmother']):
					self.result_list.append(Fraction('1/6'))
				elif not self._exist(['mother','father']) and self._exist(['maternal_grandmother']):
					self.result_list.append(Fraction('1/12'))
				else:
					self.result_list.append(Fraction('0/1'))
			
			if case == 'maternal_grandmother':
				if not self._exist(['mother', 'father', 'paternal_grandmother']):
					self.result_list.append(Fraction('1/6'))
				elif not self._exist(['mother']) and self._exist(['maternal_grandmother']):
					self.result_list.append(Fraction('1/12'))
				else:
					self.result_list.append(Fraction('0/1'))

			if case == 'brother':
				if self._exist(male_offspring) or self._exist(male_ancestor):
					self.result_list.append(Fraction('0/1'))
				else:
					self.result_list.append(Fraction('-1/1'))
			
			if case == 'sister':
				if self._exist(male_offspring) or self._exist(male_ancestor):
					self.result_list.append(Fraction('0/1'))
				elif self._exist(['father', 'son', 'brother', 'uncle']):
					self.result_list.append(Fraction('-2/1'))
				elif self._exist(['daughter']) and not self._exist(males):
					self.result_list.append(Fraction('-1/1'))
				else:
					if self.count_list[i] > 1:
						self.result_list.append(Fraction('2/3'))
					else:
						self.result_list.append(Fraction('1/2'))

			if case == 'paternal_brother':
				if (not self._exist(['brother','father'])) and (not self._exist(male_offspring)):
					self.result_list.append(Fraction('-1/1'))
				else:
					self.result_list.append(Fraction('0/2'))


			if case == 'paternal_sister':
				if not self._exist(['brother', 'grandfather']) and not self._exist(male_offspring): 
					if self._exist(['sister']) and not self._exist(['paternal_brother']):
						j = get_element_index(self.relative_list, 'sister')
						if self.count_list[j] == 1:
							self.result_list.append(Fraction('1/6'))
					elif self._exist(['paternal_brother']):
							self.result_list.append(Fraction('-2/1'))
					elif self._exist(['daughter']) and not self._exist(males):
						self.result_list.append(Fraction('-1/1'))									
					else:
						if self.count_list[i] > 1:
							self.result_list.append(Fraction('2/3'))
						else:
							self.result_list.append(Fraction('1/2'))
				else:
					self.result_list.append(Fraction('0/6'))
			
			if case == 'maternal_brother' or case == 'maternal_sister':
				if self._exist(male_offspring) or self._exist(['father', 'grandfather']):
					self.result_list.append(Fraction('0/3'))
				# if (not self._exist(['brother','father'])) and (not self._exist(offspring))\
				#   and self._exist(['paternal_brother']):
				#   self.result_list.append(Fraction('-1/1'))
				else:
					if self._count_maternal_sibling() > 1:
						self.result_list.append(Fraction('1/3'))
					else:
						self.result_list.append(Fraction('1/6'))

			if case == 'nephew':
				if self._exist(male_offspring) or self._exist(['brother', 'father', 'grandfather',\
					'paternal_brother']):
					self.result_list.append(Fraction('0/1'))
				else:
					self.result_list.append(Fraction('-1/1'))
			
			if case == 'paternal_nephew':
				if self._exist(male_offspring) or self._exist(['brother', 'father', 'grandfather',\
					'paternal_brother', 'nephew']):
					self.result_list.append(Fraction('0/1'))
				else:
					self.result_list.append(Fraction('-1/1'))
			
			if case == 'nephew_son':
				if self._exist(male_offspring) or self._exist(['brother', 'father', 'grandfather',\
					'paternal_brother', 'nephew', 'paternal_nephew']):
					self.result_list.append(Fraction('0/1'))
				else:
					self.result_list.append(Fraction('-1/1'))
			
			if case == 'paternal_nephew_son':
				if self._exist(male_offspring) or self._exist(['brother', 'father', 'grandfather',\
					'paternal_brother', 'nephew', 'paternal_nephew', 'nephew_son']):
					self.result_list.append(Fraction('0/1'))
				else:
					self.result_list.append(Fraction('-1/1'))
			
			if case == 'paternal_uncle':
				if self._exist(male_offspring) or self._exist(['brother', 'father', 'grandfather',\
					'paternal_brother', 'nephew', 'paternal_nephew', 'nephew_son',\
					'paternal_nephew_son']):
					self.result_list.append(Fraction('0/1'))
				else:
					self.result_list.append(Fraction('-1/1'))

			if case == 'paternal_paternal_uncle':
				if self._exist(male_offspring) or self._exist(['brother','father','grandfather'\
					,'paternal_brother','nephew','paternal_nephew','nephew_son'\
					,'paternal_nephew_son','paternal_uncle']):
					self.result_list.append(Fraction('0/1'))
				else:
					self.result_list.append(Fraction('-1/1'))

			if case == 'cousin':
				if self._exist(male_offspring) or self._exist(['brother','father','grandfather'\
					,'paternal_brother','nephew','paternal_nephew','nephew_son'\
					,'paternal_nephew_son','paternal_uncle','paternal_paternal_uncle']):
					self.result_list.append(Fraction('0/1'))
				else:
					self.result_list.append(Fraction('-1/1'))

			if case == 'paternal_cousin':
				if self._exist(male_offspring) or self._exist(['brother','father','grandfather'\
					,'paternal_brother','nephew','paternal_nephew','nephew_son'\
					,'paternal_nephew_son','paternal_uncle','paternal_paternal_uncle','cousin']):
					self.result_list.append(Fraction('0/1'))
				else:
					self.result_list.append(Fraction('-1/1'))
			
			if case == 'cousin_son':
				if self._exist(male_offspring) or self._exist(['brother','father','grandfather'\
					,'paternal_brother','nephew','paternal_nephew','nephew_son'\
					,'paternal_nephew_son','paternal_uncle','paternal_paternal_uncle','cousin',\
					'paternal_cousin']):
					self.result_list.append(Fraction('0/1'))
				else:
					self.result_list.append(Fraction('-1/1'))

			if case == 'paternal_cousin_son':
				if self._exist(male_offspring) or self._exist(['brother','father','grandfather'\
					,'paternal_brother','nephew','paternal_nephew','nephew_son'\
					,'paternal_nephew_son','paternal_uncle','paternal_paternal_uncle','cousin'\
					,'paternal_cousin','cousin_son']):
					self.result_list.append(Fraction('0/1'))
				else:
					self.result_list.append(Fraction('-1/1'))

			if case == 'cousin_grandson':
				if self._exist(male_offspring) or self._exist(['brother','father','grandfather'\
					,'paternal_brother','nephew','paternal_nephew','nephew_son'\
					,'paternal_nephew_son','paternal_uncle','paternal_paternal_uncle','cousin'\
					,'paternal_cousin','cousin_son','paternal_cousin_son']):
					self.result_list.append(Fraction('0/1'))
				else:
					self.result_list.append(Fraction('-1/1'))

			if case == 'paternal_cousin_grandson':
				if self._exist(male_offspring) or self._exist(['brother','father','grandfather'\
					,'paternal_brother','nephew','paternal_nephew','nephew_son'\
					,'paternal_nephew_son','paternal_uncle','paternal_paternal_uncle','cousin'\
					,'paternal_cousin','cousin_son','paternal_cousin_son','cousin_grandson']):
					self.result_list.append(Fraction('0/1'))
				else:
					self.result_list.append(Fraction('-1/1'))

		self._correct_ratio()

		#fill log with final results
		self._append_to_log('current results :')
		for i in range(len(self.result_list)):
			self._append_to_log(str(self.relative_list[i]) + ' -> ' + str(self.result_list[i]))

	def _correct_ratio(self):
		#1-calcute total
		total = Fraction('0/1')
		for i in range (len(self.result_list)):
			if self.result_list[i] > 0:
				total += self.result_list[i]
		self._append_to_log(str(self.relative_list[i]) + ' take ' + str(self.result_list[i]))

		#2-distribuate remains if there is
		#aasba male
		aasba_m = get_element_index(self.result_list, -1)
		#aasba female
		aasba_f = get_element_index(self.result_list, -2)
		if aasba_m != -1 and aasba_f != -1:
			male = self.count_list[aasba_m]
			female = self.count_list[aasba_f]
			shares = male * 2 + female
			self.result_list[aasba_m] = (Fraction('1/1') - total) * Fraction(male*2, shares)
			self.result_list[aasba_f] = (Fraction('1/1') - total) * Fraction(female, shares)         
			self._append_to_log(str(self.relative_list[aasba_m]) + ' and ' + str(self.relative_list[aasba_f]) + ' take the remain')
			return
		if aasba_m != -1 and aasba_f == -1:
			self.result_list[aasba_m] = Fraction('1/1') - total
			self._append_to_log(str(self.relative_list[aasba_m]) + ' take remain')
			
			#maternal sibling can't  have more than other sibling
			f_brother = get_element_index(self.relative_list, "brother")
			p_brother = get_element_index(self.relative_list, "paternal_brother")
			m_brother = get_element_index(self.relative_list, "maternal_brother")
			if (f_brother != -1 or p_brother != -1) and m_brother != -1:
				o_brother = f_brother
				if f_brother == -1:
					o_brother = p_brother
				if self.result_list[m_brother] > self.result_list[o_brother]:
					total = self.result_list[m_brother] + self.result_list[o_brother]
					self.result_list[o_brother] = total / 2
					self.result_list[m_brother] = total / 2
			return
		
		male_offspring = ['son', 'grandson']
		if total < 1 and self._exist(['father']) and not self._exist(male_offspring):
			idx = get_element_index(self.relative_list, 'father')
			self.result_list[idx] += Fraction(1,1) - total
			return

		#3-equalify the shares if necesary
		sub_total = total
		tot = Fraction(0, 1)
		if total != 1:
			#wife and husband cannot have higher share than precripted
			spouse = ''
			if self._exist(['wife']):
				spouse = 'wife'
			elif self._exist(['husband']):
				spouse = 'husband'
				
			if self._exist([spouse]):
				idx = get_element_index(self.relative_list, spouse)
				sub_total -= self.result_list[idx]
			self._append_to_log('correting total')
			for i in range(len(self.result_list)):
				if self._exist([spouse]) and total < 1:
					if self.relative_list[i] == spouse:
						pass
						#self.result_list[i] = Fraction(1, 8)
					else:
						idx = get_element_index(self.relative_list, spouse)
						remain = Fraction(1, 1) - total
						self.result_list[i] *= Fraction(sub_total + remain, sub_total)
						#self.result_list[i] *= Fraction(sub_total + remain, sub_total)
						#self.result_list[i] *= Fraction(Fraction(1, 1) - self.result_list[idx], sub_total)
				else:
					self.result_list[i] *= Fraction(total.denominator, total.numerator)
				tot += self.result_list[i]
				self._append_to_log(str(self.relative_list[i]) + ' take ' + str(self.result_list[i]))
		self._append_to_log('total corrected = ' + str(tot))

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




#====================    self-test section        ====================
'''
Test cases was taken from the book
"THE FINAL BEQUEST: THE ISLAMIC WILL & TESTAMENT" by MUHAMMAD AL-JIBALI
67-75 82-90
'''
cases = 0
#used by test_mirath_cases()
def check_results(case, true_result):
	if case.result_list == true_result:
		print(case.name + " is correct")
	else:
		#print(case.name + " is incorrect")
		print("incorrect results in " + case.name + "")
		print("what you have :        " + str(case.result_list))
		print("what you should have :     " + str(true_result))
		global cases
		cases += 1

#main testing function
def test_mirath_cases():
	'''
	Please notice that the order of adding relative is
	very crucial in this test, as the referential result
	(true_result) are given accordinately to the order of
	current relatives.
	'''
	#test case 1

	cases = 0

	case = Mirath("case 1")
	case.add_relative('wife')
	case.add_relative('mother')
	case.add_relative('son')
	case.calculate_mirath()

	true_result = [Fraction(3, 24), Fraction(4, 24), Fraction(17, 24)]
	check_results(case, true_result)

	#test case 2

	case = Mirath("case 2")
	case.add_relative('husband')
	case.add_relative('sister', 2)
	case.calculate_mirath()

	true_result = [Fraction(3, 7), Fraction(4, 7)]
	check_results(case, true_result)

	#test case 3

	case = Mirath("case 3")
	case.add_relative('husband')
	case.add_relative('mother')
	case.add_relative('father')
	case.calculate_mirath()

	true_result = [Fraction(3, 6), Fraction(1, 6), Fraction(2, 6)]
	check_results(case, true_result)

	#test case 4

	case = Mirath("case 4")
	case.add_relative('wife')
	case.add_relative('mother')
	case.add_relative('father')
	case.calculate_mirath()

	true_result = [Fraction(1, 4), Fraction(1, 4), Fraction(2, 4)]
	check_results(case, true_result)

	#test case 5

	case = Mirath("case 5")
	case.add_relative('husband')
	case.add_relative('mother')
	case.add_relative('maternal_brother', 2)
	case.add_relative('paternal_brother', 2)
	case.calculate_mirath()

	true_result = [Fraction(6, 12), Fraction(2, 12), Fraction(2, 12), Fraction(2, 12)]
	check_results(case, true_result)

	#test case 6

	case = Mirath("case 6")
	case.add_relative('mother')
	case.add_relative('sister')
	case.calculate_mirath()

	true_result = [Fraction(2, 5), Fraction(3, 5)]
	check_results(case, true_result)

	#test case 7

	case = Mirath("case 7")
	case.add_relative('maternal_grandmother')
	case.add_relative('sister')
	case.add_relative('maternal_brother')
	case.calculate_mirath()

	true_result = [Fraction(1, 5), Fraction(3, 5), Fraction(1, 5)]
	check_results(case, true_result)

	#test case 8

	case = Mirath("case 8")
	case.add_relative('daughter')
	case.add_relative('granddaughter', 2)
	case.calculate_mirath()

	true_result = [Fraction(6, 8), Fraction(2, 8)]
	check_results(case, true_result)

	#test case 9

	case = Mirath("case 9")
	case.add_relative('mother')
	case.add_relative('maternal_brother', 3)
	case.calculate_mirath()

	true_result = [Fraction(3, 9), Fraction(6, 9)]
	check_results(case, true_result)

	#test case 10

	case = Mirath("case 10")
	case.add_relative('wife')
	case.add_relative('sister', 2)
	case.calculate_mirath()

	true_result = [Fraction(2, 8), Fraction(6, 8)]
	check_results(case, true_result)

	#test case 11 p73

	case = Mirath("case 11")
	case.add_relative('wife')
	case.add_relative('daughter')
	case.add_relative('mother')
	case.calculate_mirath()

	true_result = [Fraction(4, 32), Fraction(21, 32), Fraction(7, 32)]
	check_results(case, true_result)

	#test case 12 p73

	case = Mirath("case 12")
	case.add_relative('wife')
	case.add_relative('mother')
	case.add_relative('maternal_brother')
	case.calculate_mirath()

	true_result = [Fraction(1, 4), Fraction(2, 4), Fraction(1, 4)]
	check_results(case, true_result)

	#test case 13 p74

	case = Mirath("case 13")
	case.add_relative('wife', 2)
	case.add_relative('maternal_brother', 2)
	case.add_relative('paternal_grandmother')
	case.add_relative('maternal_grandmother')
	case.calculate_mirath()

	true_result = [Fraction(2, 8), Fraction(4, 8), Fraction(1, 8), Fraction(1, 8)]
	check_results(case, true_result)

	#test case 14 p75

	case = Mirath("case 14")
	case.add_relative('wife')
	case.add_relative('daughter')
	case.add_relative('mother')
	case.add_relative('brother')
	case.calculate_mirath()

	true_result = [Fraction(3, 24), Fraction(12, 24), Fraction(4, 24), Fraction(5, 24)]
	check_results(case, true_result)

	#test case 15 p82 ????????????????

	case = Mirath("case 15")
	case.add_relative('paternal_maternal_uncle')
	case.add_relative('sister', 2)
	case.add_relative('maternal_sister', 2)
	case.calculate_mirath()

	true_result = [Fraction(1, 7), Fraction(4, 7), Fraction(2, 7)]
	check_results(case, true_result)

# chap 5

	#test case 16 p83

	case = Mirath("case 16")
	case.add_relative('wife')
	case.add_relative('mother')
	case.add_relative('daughter')
	case.add_relative('paternal_uncle')
	case.calculate_mirath()

	true_result = [Fraction(3, 24), Fraction(4, 24), Fraction(12, 24), Fraction(5, 24)]
	check_results(case, true_result)

	#test case 17 p83

	case = Mirath("case 17")
	case.add_relative('wife')
	case.add_relative('daughter')
	case.add_relative('brother')
	case.add_relative('paternal_uncle')
	case.calculate_mirath()

	true_result = [Fraction(3, 24), Fraction(12, 24), Fraction(9, 24), Fraction(0, 24)]
	check_results(case, true_result)

	#test case 18 p84

	case = Mirath("case 18")
	case.add_relative('wife')
	case.add_relative('brother', 2)
	case.add_relative('sister')
	case.add_relative('paternal_uncle')
	case.calculate_mirath()

	true_result = [Fraction(5, 20), Fraction(12, 20), Fraction(3, 20), Fraction(0, 24)]
	check_results(case, true_result)

	#test case 19 p84

	case = Mirath("case 19")
	case.add_relative('daughter')
	case.add_relative('granddaughter')
	case.add_relative('sister', 2)
	case.calculate_mirath()

	true_result = [Fraction(6, 12), Fraction(2, 12), Fraction(4, 12)]
	check_results(case, true_result)

	#test case 20 p84

	case = Mirath("case 20")
	case.add_relative('wife', 2)
	case.add_relative('daughter')
	case.add_relative('father')
	case.add_relative('brother')
	case.calculate_mirath()

	true_result = [Fraction(1, 8), Fraction(4, 8), Fraction(3, 8), Fraction(0, 8)]
	check_results(case, true_result)

	#test case 21 p85

	case = Mirath("case 21")
	case.add_relative('husband')
	case.add_relative('daughter')
	case.add_relative('father')
	case.calculate_mirath()

	true_result = [Fraction(2, 8), Fraction(4, 8), Fraction(2, 8)]
	check_results(case, true_result)

	#test case 22 p85

	case = Mirath("case 22")
	case.add_relative('husband')
	case.add_relative('mother')
	case.add_relative('daughter')
	case.add_relative('sister')
	case.calculate_mirath()

	true_result = [Fraction(3, 12), Fraction(2, 12), Fraction(6, 12), Fraction(1, 12)]
	check_results(case, true_result)

	#test case 23 p85

	case = Mirath("case 23")
	case.add_relative('husband')
	case.add_relative('granddaughter')
	case.add_relative('cousin')
	case.calculate_mirath()

	true_result = [Fraction(1, 4), Fraction(2, 4), Fraction(1, 4)]
	check_results(case, true_result)

	#test case 24 p85
	#skip emancipator's case
	
	#test case 25 p85
	#skip emancipator's case
	
	#test case 26 p86
	#pass emancipator's case

	#test case 27 p86

	case = Mirath("case 27")
	case.add_relative('son', 3)
	case.calculate_mirath()

	true_result = [Fraction(1, 1)]
	check_results(case, true_result)

	#test case 28 p86

	case = Mirath("case 28")
	case.add_relative('wife')
	case.add_relative('son')
	case.add_relative('daughter')
	case.calculate_mirath()

	true_result = [Fraction(3, 24), Fraction(14, 24), Fraction(7, 24)]
	check_results(case, true_result)

	#test case 29 p86

	case = Mirath("case 29")
	case.add_relative('son')
	case.add_relative('daughter', 2)
	case.calculate_mirath()

	true_result = [Fraction(2, 4), Fraction(2, 4)]
	check_results(case, true_result)

	#test case 30 p86

	case = Mirath("case 30")
	case.add_relative('husband')
	case.add_relative('son')
	case.add_relative('daughter')
	case.calculate_mirath()

	true_result = [Fraction(1, 4), Fraction(2, 4), Fraction(1, 4)]
	check_results(case, true_result)

	#test case 31 p86

	case = Mirath("case 31")
	case.add_relative('brother', 2)
	case.add_relative('sister')
	case.calculate_mirath()

	true_result = [Fraction(4, 5), Fraction(1, 5)]
	check_results(case, true_result)

	#test case 32 p86

	case = Mirath("case 32")
	case.add_relative('mother')
	case.add_relative('maternal_brother')
	case.add_relative('brother')
	case.calculate_mirath()

	true_result = [Fraction(1, 6), Fraction(1, 6), Fraction(4, 6)]
	check_results(case, true_result)

	#test case 33 p87

	case = Mirath("case 33")
	case.add_relative('mother')
	case.add_relative('daughter')
	case.add_relative('paternal_brother')
	case.calculate_mirath()

	true_result = [Fraction(1, 6), Fraction(3, 6), Fraction(2, 6)]
	check_results(case, true_result)

	#test case 34 p87

	case = Mirath("case 34")
	case.add_relative('husband')
	case.add_relative('mother')
	case.add_relative('brother')
	case.calculate_mirath()

	true_result = [Fraction(3, 6), Fraction(2, 6), Fraction(1, 6)]
	check_results(case, true_result)

	#test case 35 p87

	case = Mirath("case 35")
	case.add_relative('wife')
	case.add_relative('daughter')
	case.add_relative('paternal_brother')
	case.calculate_mirath()

	true_result = [Fraction(1, 8), Fraction(4, 8), Fraction(3, 8)]
	check_results(case, true_result)

	#test case 36 p87

	case = Mirath("case 36")
	case.add_relative('wife')
	case.add_relative('mother')
	case.add_relative('daughter')
	case.add_relative('granddaughter')
	case.add_relative('brother')
	case.calculate_mirath()

	true_result = [Fraction(3, 24), Fraction(4, 24), Fraction(12, 24), Fraction(4, 24), Fraction(1, 24)]
	check_results(case, true_result)

	#test case 37 p87

	case = Mirath("case 37")
	case.add_relative('wife')
	case.add_relative('mother')
	case.add_relative('son')
	case.calculate_mirath()

	true_result = [Fraction(3, 24), Fraction(4, 24), Fraction(17, 24)]
	check_results(case, true_result)

	#test case 38 p87

	case = Mirath("case 38")
	case.add_relative('wife')
	case.add_relative('daughter', 3)
	case.add_relative('brother')
	case.calculate_mirath()

	true_result = [Fraction(9, 72), Fraction(48, 72), Fraction(15, 72)]
	check_results(case, true_result)

	#test case 39 p87

	case = Mirath("case 39")
	case.add_relative('husband')
	case.add_relative('sister')
	case.calculate_mirath()

	true_result = [Fraction(1, 2), Fraction(1, 2)]
	check_results(case, true_result)

	#test case 40 p87

	case = Mirath("case 40")
	case.add_relative('wife')
	case.add_relative('mother')
	case.add_relative('daughter')
	case.add_relative('brother')
	case.calculate_mirath()

	true_result = [Fraction(3, 24), Fraction(4, 24), Fraction(12, 24), Fraction(5, 24)]
	check_results(case, true_result)

	#test case 41 p87

	case = Mirath("case 41")
	case.add_relative('wife')
	case.add_relative('father')
	case.add_relative('son')
	case.add_relative('paternal_nephew')
	case.calculate_mirath()

	true_result = [Fraction(3, 24), Fraction(4, 24), Fraction(17, 24), Fraction(0, 24)]
	check_results(case, true_result)

	#test case 42 p88

	case = Mirath("case 42")
	case.add_relative('wife')
	case.add_relative('daughter', 3)
	case.add_relative('maternal_grandmother')
	case.add_relative('brother')
	case.calculate_mirath()

	true_result = [Fraction(9, 72), Fraction(48, 72), Fraction(12, 72), Fraction(3, 72)]
	check_results(case, true_result)

	#test case 43 p88

	case = Mirath("case 43")
	case.add_relative('wife', 2)
	case.add_relative('brother')
	case.add_relative('sister', 2)
	case.calculate_mirath()

	true_result = [Fraction(4, 16), Fraction(6, 16), Fraction(6, 16)]
	check_results(case, true_result)

	#test case 44 p88

	case = Mirath("case 44")
	case.add_relative('wife', 2)
	case.add_relative('brother')
	case.add_relative('sister', 2)
	case.calculate_mirath()

	true_result = [Fraction(4, 16), Fraction(6, 16), Fraction(6, 16)]
	check_results(case, true_result)

	#test case 45 p88

	case = Mirath("case 45")
	case.add_relative('daughter', 3)
	case.add_relative('paternal_uncle')
	case.calculate_mirath()

	true_result = [Fraction(6, 9), Fraction(3, 9)]
	check_results(case, true_result)

	#test case 46 p88

	case = Mirath("case 46")
	case.add_relative('daughter', 3)
	case.add_relative('sister', 3)
	case.calculate_mirath()

	true_result = [Fraction(6, 9), Fraction(3, 9)]
	check_results(case, true_result)

	#test case 47 p88

	case = Mirath("case 47")
	case.add_relative('wife', 2)
	case.add_relative('sister', 3)
	case.add_relative('paternal_brother', 3)
	case.calculate_mirath()

	true_result = [Fraction(18, 72), Fraction(48, 72), Fraction(6, 72)]
	check_results(case, true_result)

	#test case 48 p88

	case = Mirath("case 48")
	case.add_relative('mother')
	case.add_relative('daughter')
	case.add_relative('granddaughter')
	case.add_relative('paternal_sister', 2)
	case.calculate_mirath()

	true_result = [Fraction(2, 12), Fraction(6, 12), Fraction(2, 12), Fraction(2, 12)]
	check_results(case, true_result)

	#test case 49 p89

	case = Mirath("case 49")
	case.add_relative('wife', 2)
	case.add_relative('maternal_grandmother', 3)
	case.add_relative('maternal_brother', 3)
	case.add_relative('paternal_uncle', 2)
	case.calculate_mirath()

	true_result = [Fraction(18, 72), Fraction(12, 72), Fraction(24, 72), Fraction(18, 72)]
	check_results(case, true_result)

	#test case 50 p89

	case = Mirath("case 50")
	case.add_relative('husband')
	case.add_relative('mother')
	case.add_relative('father')
	case.add_relative('son', 2)
	case.add_relative('daughter', 3)
	case.add_relative('grandfather')
	case.add_relative('brother')
	case.calculate_mirath()

	true_result = [Fraction(21, 84), Fraction(14, 84), Fraction(14, 84), Fraction(20, 84), Fraction(15, 84), Fraction(0, 84), Fraction(0, 84)]
	check_results(case, true_result)

	#test case 51 p89

	case = Mirath("case 51")
	case.add_relative('husband')
	case.add_relative('sister')
	case.add_relative('paternal_sister')
	case.add_relative('mother')
	case.add_relative('maternal_sister', 2)
	case.calculate_mirath()


	true_result = [Fraction(3, 10), Fraction(3, 10), Fraction(1, 10), Fraction(1, 10), Fraction(2, 10)]
	check_results(case, true_result)

	#test case 52 p89

	case = Mirath("case 52")
	case.add_relative('husband')
	case.add_relative('paternal_sister', 2)
	case.add_relative('maternal_brother', 2)
	case.calculate_mirath()

	true_result = [Fraction(3, 9), Fraction(4, 9), Fraction(2, 9)]
	check_results(case, true_result)

	#test case 53 p90

	case = Mirath("case 53")
	case.add_relative('husband')
	case.add_relative('sister')
	case.add_relative('paternal_grandmother')
	case.calculate_mirath()

	true_result = [Fraction(3, 7), Fraction(3, 7), Fraction(1, 7)]
	check_results(case, true_result)

	#test case 54 p90

	case = Mirath("case 54")
	case.add_relative('wife')
	case.add_relative('paternal_sister', 2)
	case.add_relative('mother')
	case.calculate_mirath()

	true_result = [Fraction(3, 13), Fraction(8, 13), Fraction(2, 13)]
	check_results(case, true_result)

	#test case 55 p90

	case = Mirath("case 55")
	case.add_relative('wife')
	case.add_relative('paternal_sister', 2)
	case.add_relative('maternal_brother', 2)
	case.add_relative('mother')
	case.calculate_mirath()

	true_result = [Fraction(3, 17), Fraction(8, 17), Fraction(4, 17), Fraction(2, 17)]
	check_results(case, true_result)

	#test case 56 p90

	case = Mirath("case 56")
	case.add_relative('wife')
	case.add_relative('sister', 2)
	case.add_relative('maternal_brother', 2)
	case.calculate_mirath()

	true_result = [Fraction(3, 15), Fraction(8, 15), Fraction(4, 15)]
	check_results(case, true_result)

	#test case 57 p90

	case = Mirath("case 57")
	case.add_relative('husband')
	case.add_relative('sister', 2)
	case.add_relative('paternal_grandmother')
	case.calculate_mirath()

	true_result = [Fraction(3, 8), Fraction(4, 8), Fraction(1, 8)]
	check_results(case, true_result)

	#test case 58 p90

	case = Mirath("case 58")
	case.add_relative('wife')
	case.add_relative('daughter', 2)
	case.add_relative('mother')
	case.add_relative('father')
	case.calculate_mirath()

	true_result = [Fraction(3, 27), Fraction(16, 27), Fraction(4, 27), Fraction(4, 27)]
	check_results(case, true_result)


	#Imam SHQAFII special case

	case = Mirath("IMAME SHAAFII case")
	case.add_relative('daughter', 2)
	case.add_relative('mother')
	case.add_relative('wife')
	case.add_relative('brother', 12)
	case.add_relative('sister')
	case.calculate_mirath()

	true_result = [Fraction(400, 600), Fraction(100, 600), Fraction(75, 600), Fraction(24, 600), Fraction(1, 600)]
	check_results(case, true_result)
