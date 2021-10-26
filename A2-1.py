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

def order_a(assignment, domain, day, slot):
	new_domain = []
	s = getSlot(slot)
	if(s == 'A' or s == 'E' or s == 'M'):
		return domain[day][slot]

	r_dict = {}
	new_domain = []
	start = day - day%7
	end = start + 7
	if(end > D):
		return domain[day][slot]
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
	# if(s != 'R'):
	# 	new_domain = new_domain[::-1]

	return new_domain

def order_b(assignment, domain, day, slot):
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

def rosterSystem(assignment, domain, part):
	# global calls
	# calls += 1
	if(complete(assignment)):
		return assignment
	(day, slot) = selectUnassignedVariable(assignment, domain)
	domain_order = []
	if(part == 0):
		domain_order = order_a(assignment, domain, day, slot)
	else:
		domain_order = order_b(assignment, domain, day, slot)
	for val in domain_order:
		if(satisfyConstraints(assignment, val, day, slot)):
			assignment[day][slot] = val
			inferences = inference(assignment, domain, val, day, slot)
			if(inferences != False):
				# print(assignment)
				# print(inferences)
				# print("----------")
				result = rosterSystem(assignment, inferences, part)
				if(result != False):
					return result
			assignment[day][slot] = None
	return False

def valid(d):
	for i in d:
		rest = 0
		for j in range(len(d[i])):
			if(d[i][j] == 'R'):
				rest += 1
			if(j > 0 and d[i][j] == 'M' and d[i][j - 1] == 'M'):
				return False
			if(j > 0 and d[i][j] == 'M' and d[i][j - 1] == 'E'):
				return False
			if((j + 1)%7 == 0):
				if(rest == 0):
					return False
				rest = 0
	for j in range(D):
		M = 0
		A = 0
		E = 0
		R = 0
		for i in d:
			if(d[i][j] == 'M'):
				M += 1
			elif(d[i][j] == 'A'):
				A += 1
			elif(d[i][j] == 'E'):
				E += 1
			else:
				R += 1
		if(M != m or A != a or E != e or R != r):
			return False
	return True

def weight(d):
	count = 0
	for i in d:
		for j in d[i]:
			if(i < S and (j == 'M' or j == 'E')):
				count += 1
	return count
	
N = 0
D = 0
m = 0
a = 0
e = 0
S = 0

# 0 for Part-a, 1 for Part-b
part = -1
file = sys.argv[1]
df = pd.read_csv(file)

if(len(df.columns) == 5):
	for index,row in df.iterrows():
		N = row['N']
		D = row['D']
		m = row['m']
		a = row['a']
		e = row['e']
		part = 0
else:
	for index,row in df.iterrows():
		N = row['N']
		D = row['D']
		m = row['m']
		a = row['a']
		e = row['e']
		S = row['S']
		part = 1

sys.setrecursionlimit(10000)
total_rest = D*(N - (m + a + e))
r = N - (m + a + e)
assignment = [[None for i in range(N)] for j in range(D)]
x = [i for i in range(N)]
domain = [[x for i in range(N)] for j in range(D)]
calls = 0

# if(part == 0 and N == 7*r):
# 	n = 0
# 	for day in range(7):
# 		for i in range(m + a + e, N):
# 			assignment[day][i] = n
# 			domain[day][i] = [n]
# 			n += 1
soln_list = [{}]
with open("solution.json" , 'w') as file:
   for d in soln_list:
       json.dump(d,file)
       file.write("\n")
if((D > 6 and N == m + a + e) or (D > 6 and N > 7*r) or (m > a + r)):
	exit(-1)

result = rosterSystem(assignment, domain, part)

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
	temp = {}
	for i in sorted(n_dict):
		for j in range(len(n_dict[i])):
			key = 'N' + str(i) + '_' + str(j)
			temp[key] = n_dict[i][j]
	soln_list.append(temp)

	with open("solution.json" , 'w') as file:
	   for d in soln_list:
	       json.dump(d,file)
	       file.write("\n")
# else:
# 	print("F")

# print(part)
# print("Time: " + str(time.time() - start_time))
# print("Calls: " + str(calls))
# print("Weight:" + str(weight(n_dict)))
# print("Validity: ", valid(n_dict))
# if(valid(n_dict) == False):
# 	print("F\n"*5)