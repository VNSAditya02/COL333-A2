import copy
import sys
import time
import pandas as pd
import json

start_time = time.time()

def complete(assignment):
	for ass in assignment:
		for d in ass:
			if(d == None):
				return False
	return True

def getSlot(slot):
	s = 'R'
	if(slot >= 0 and slot < m):
		s = 'M'
	elif(slot >= m and slot < m + a):
		s = 'A'
	elif(slot >= m + a and slot < m + a + e):
		s = 'E'
	return s

def selectUnassignedVariable1(assignment, domain):
	min_val = float('inf')
	for day in range(len(assignment)):
		for slot in range(0, m):
			if(assignment[day][slot] == None):
				return (day, slot)

	for day in range(len(assignment)):
		for slot in range(m + a + e, N):
			if(assignment[day][slot] == None):
				return (day, slot)

	# for day in range(len(assignment)):
	# 	for slot in range(m, m + a):
	# 		if(assignment[day][slot] == None):
	# 			return (day, slot)
	# for day in range(len(assignment)):
	# 	for slot in range(m + a, m + a + e):
	# 		if(assignment[day][slot] == None):
	# 			return (day, slot)

	for i in range(len(assignment)):
		for j in range(len(assignment[i])):
			if(assignment[i][j] == None):
				return (i, j)

def selectUnassignedVariable(assignment, domain):
	min_val = float('inf')
	cur_slot = None
	for i in range(len(assignment)):
		for j in range(len(assignment[i])):
			if(assignment[i][j] == None and len(domain[i][j]) < min_val):
				cur_slot = getSlot(j)
				min_val = len(domain[i][j])
				min_i = i
				min_j = j
			elif(assignment[i][j] == None and len(domain[i][j]) == min_val and getSlot(j) == 'R' and cur_slot != 'R'):
				cur_slot = getSlot(j)
				min_val = len(domain[i][j])
				min_i = i
				min_j = j
			# elif(assignment[i][j] == None and len(domain[i][j]) < min_val):
			# 	cur_slot = getSlot(j)
			# 	min_val = len(domain[i][j])
			# 	min_i = i
			# 	min_j = j
			# elif(assignment[i][j] == None and len(domain[i][j]) == min_val and getSlot(j) == 'M' and cur_slot != 'M' and cur_slot != 'R'):
			# 	cur_slot = getSlot(j)
			# 	min_val = len(domain[i][j])
			# 	min_i = i
			# 	min_j = j
			# elif(assignment[i][j] == None and len(domain[i][j]) == min_val and getSlot(j) == 'E' and cur_slot != 'M' and cur_slot != 'E' and cur_slot != 'R'):
			# 	cur_slot = getSlot(j)
			# 	min_val = len(domain[i][j])
			# 	min_i = i
			# 	min_j = j
	return (min_i, min_j)

def isLastAssignment(assignment, day):
	c = 0
	start = day - day%7
	end = start + 7
	if(end > D):
		return False
	for day in range(start, end):
		ass = assignment[day][m + a + e:]
		for slot in ass:
			if(slot == None):
				c += 1
	if(c == 1):
		return True
	return False

def satisfyConstraints(assignment, val, day, slot):
	s = getSlot(slot)

	prev_m = assignment[day - 1][:m]
	prev_a = assignment[day - 1][m:m + a]
	prev_e = assignment[day - 1][m + a:m + a + e]
	prev_r = assignment[day - 1][m + a + e:]
	if(day > 0 and s == 'M' and val in prev_m):
		return False
	if(day > 0 and s == 'M' and val in prev_e):
		return False
	if(val in assignment[day]):
		return False

	# r_dict = {}
	# c = 0
	# for d in range(D):
	# 	r_slot = assignment[d][m + a + e:]
	# 	for p in r_slot:
	# 		if(p != None):
	# 			c += 1
	# 		if p in r_dict:
	# 			r_dict[p] += 1
	# 		else:
	# 			r_dict[p] = 1
	# if(s == 'R'):
	# 	c += 1
	# 	if val in r_dict:
	# 		r_dict[val] += 1
	# 	else:
	# 		r_dict[val] = 1
	# if(N - len(r_dict) > total_rest - c):
	# 	return False

	if(isLastAssignment(assignment, day) and s == 'R'):
		r_dict = {}
		start = day - day%7
		end = start + 7
		for d in range(start, end):
			r_slot = assignment[d][m + a + e:]
			for p in r_slot:
				if p in r_dict:
					r_dict[p] += 1
				else:
					r_dict[p] = 1
		if(s == 'R'):
			if val in r_dict:
				r_dict[val] += 1
			else:
				r_dict[val] = 1
		for v in range(N):
			if(v not in r_dict):
				return False
	return True

def inference(assignment, domain, val, day, slot):
	new_domain = copy.deepcopy(domain)
	new_domain[day][slot] = [val]
	s = getSlot(slot)
	x = len(new_domain[day])
	for i in range(x):
		if(i != slot and val in new_domain[day][i]):
			new_domain[day][i] = [x for x in new_domain[day][i] if x != val]

	if(s == 'M' and day < D - 1):
		for i in range(m):
			if(val in new_domain[day + 1][i]):
				new_domain[day + 1][i] = [x for x in new_domain[day + 1][i] if x != val]
				if(len(new_domain[day + 1][i]) == 0):
					return False

	if(s == 'M' and day > 0):
		for i in range(m):
			if(val in new_domain[day - 1][i]):
				new_domain[day - 1][i] = [x for x in new_domain[day - 1][i] if x != val]
				if(len(new_domain[day - 1][i]) == 0):
					return False

	if(s == 'M' and day > 0):
		for i in range(m + a, m + a + e):
			if(val in new_domain[day - 1][i]):
				new_domain[day - 1][i] = [x for x in new_domain[day - 1][i] if x != val]
				if(len(new_domain[day - 1][i]) == 0):
					return False

	if(s == 'E' and day < D - 1):
		for i in range(m):
			if(val in new_domain[day + 1][i]):
				new_domain[day + 1][i] = [x for x in new_domain[day + 1][i] if x != val]
				if(len(new_domain[day + 1][i]) == 0):
					return False
	return new_domain

def order(assignment, domain, day, slot):

	s = getSlot(slot)
	if(s == 'E' or s == 'M'):
		new_domain1 = copy.deepcopy(domain[day][slot])
		temp = []
		for per in range(S):
			if(per in new_domain1):
				new_domain1.remove(per)
				temp.append(per)
		new_domain1 = temp + new_domain1
		return new_domain1

	if(s == 'A'):
		new_domain1 = copy.deepcopy(domain[day][slot])
		temp = []
		for per in range(S):
			if(per in new_domain1):
				new_domain1.remove(per)
				temp.append(per)
		new_domain1 = new_domain1 + temp
		return new_domain1

	r_dict = {}
	new_domain = []
	start = day - day%7
	end = start + 7
	if(end > D):
		new_domain1 = copy.deepcopy(domain[day][slot])
		temp = []
		for per in range(S):
			if(per in new_domain1):
				new_domain1.remove(per)
				temp.append(per)
		new_domain1 = new_domain1 + temp
		return new_domain1

	for d in range(start, end):
		r_slot = assignment[d][m + a + e:]
		for p in r_slot:
			if p in r_dict:
				r_dict[p] += 1
			else:
				r_dict[p] = 1
	for v in range(N):
		if(v not in r_dict and v in domain[day][slot]):
			new_domain.append(v)
	r_dict = {k: v for k, v in sorted(r_dict.items(), key=lambda item: item[1])}
	for v in range(N):
		if(v in r_dict and v in domain[day][slot]):
			new_domain.append(v)

	new_domain1 = copy.deepcopy(new_domain)
	temp = []
	for per in range(S):
		if(per in new_domain1 and per in r_dict):
			new_domain1.remove(per)
			temp.append(per)
	new_domain1 = new_domain1 + temp
	return new_domain1

def rosterSystem(assignment, domain):
	global calls
	calls += 1
	if(time.time() - start_time > 300):
		print("TLE")
		exit(-1)
	# print("Calls: " + str(calls))
	if(complete(assignment)):
		return assignment
	(day, slot) = selectUnassignedVariable(assignment, domain)
	for val in order(assignment, domain, day, slot):
		if(satisfyConstraints(assignment, val, day, slot)):
			assignment[day][slot] = val
			inferences = inference(assignment, domain, val, day, slot)
			
			if(inferences != False):
				# print(assignment)
				# print(inferences)
				# print("----------")
				result = rosterSystem(assignment, inferences)
				if(result != False):
					return result
			assignment[day][slot] = None
	return False

def weight(d):
	weight = 1
	for i in d:
		for j in d[i]:
			# print(i, d[i])
			if(i < S and (j == 'M' or j == 'E')):
				weight *= 2
	return weight

N = 0
D = 0
m = 0
a = 0
e = 0
S = 0
T = 0

df = pd.read_csv('input1.csv')
for index,row in df.iterrows():
	N = row['N']
	D = row['D']
	m = row['m']
	a = row['a']
	e = row['e']
	S = row['S']
	T = row['T']

# N = 40
# D = 36
# m = 20
# a = 10
# e = 5

sys.setrecursionlimit(10000)
total_rest = D*(N - (m + a + e))
r = N - (m + a + e)
assignment = [[None for i in range(N)] for j in range(D)]
x = [i for i in range(N)]
domain = [[x for i in range(N)] for j in range(D)]
calls = 0

soln_list = [{}]
with open("solution1.json" , 'w') as file:
   for d in soln_list:
       json.dump(d,file)
       file.write("\n")
if((D > 6 and N == m + a + e) or (N > 7*r) or (m > a + r)):
	exit(-1)
result = rosterSystem(assignment, domain)
n_dict = {}
if(result != False):
	soln_list = []
	
	for day in result:
		for slot in range(len(day)):
			s = getSlot(slot)
			per = day[slot]
			if per in n_dict:
				n_dict[per].append(s)
			else:
				n_dict[per] = [s]
	for i in sorted(n_dict):
		temp = {}
		for j in range(len(n_dict[i])):
			key = 'N' + str(i) + '_' + str(j)
			temp[key] = n_dict[i][j]
		soln_list.append(temp)

	with open("solution1.json" , 'w') as file:
	   for d in soln_list:
	       json.dump(d,file)
	       file.write("\n")
else:
	print("F")

		
print("Time: " + str(time.time() - start_time))
print("Calls: " + str(calls))
print("Weight:" + str(weight(n_dict)))