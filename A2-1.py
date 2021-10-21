import copy
import sys
import time

start_time = time.time()
N = 12
D = 99
m = 2
a = 1
e = 1
# N = 40
# D = 36
# m = 20
# a = 10
# e = 5

sys.setrecursionlimit(5000)
total_rest = D*(N - (m + a + e))
# m_slot = [None for i in range(m)]
# a_slot = [None for i in range(a)]
# e_slot = [None for i in range(e)]
# r_slot =
assignment = [[None for i in range(N)] for j in range(D)]
x = [i for i in range(N)]
domain = [[x for i in range(N)] for j in range(D)]
queue = []
neighbours = [[[None] for i in range(N)] for j in range(D)]
calls = 0

for d in range(D):
	for i in range(N):
		for j in range(i + 1, N):
			queue.append(((d, i), (d, j)))
			queue.append(((d, j), (d, i)))
			neighbours[d][i].append((d, j))
			neighbours[d][j].append((d, i))

for d in range(1, D):
	for i in range(m):
		for j in range(m):
			queue.append(((d, i), (d - 1, j)))
			queue.append(((d - 1, j), (d, i)))
			neighbours[d - 1][j].append((d, i))
			neighbours[d][i].append((d - 1, j))
		for j in range(m + a, m + a + e):
			queue.append(((d, i), (d - 1, j)))
			queue.append(((d - 1, j), (d, i)))
			neighbours[d - 1][j].append((d, i))
			neighbours[d][i].append((d - 1, j))

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

def selectUnassignedVariable(assignment, domain):
	# min_val = float('inf')
	# for day in range(len(assignment)):
	# 	for slot in range(0, m):
	# 		if(assignment[day][slot] == None):
	# 			return (day, slot)

	# for day in range(len(assignment)):
	# 	for slot in range(m + a + e, N):
	# 		if(assignment[day][slot] == None):
	# 			return (day, slot)

	# for day in range(len(assignment)):
	# 	for slot in range(m + a, m + a + e):
	# 		if(assignment[day][slot] == None):
	# 			return (day, slot)

	# for i in range(len(assignment)):
	# 	for j in range(len(assignment[i])):
	# 		if(assignment[i][j] == None):
	# 			return (i, j)
	min_val = float('inf')
	cur_slot = None
	for i in range(len(assignment)):
		for j in range(len(assignment[i])):
			if(assignment[i][j] == None and len(domain[i][j]) < min_val):
				cur_slot = getSlot(j)
				min_val = len(domain[i][j])
				min_i = i
				min_j = j
			elif(assignment[i][j] == None and len(domain[i][j]) == min_val and getSlot(j) == 'M' and cur_slot != 'M'):
				cur_slot = getSlot(j)
				min_val = len(domain[i][j])
				min_i = i
				min_j = j
			elif(assignment[i][j] == None and len(domain[i][j]) == min_val and getSlot(j) == 'E' and cur_slot != 'M' and cur_slot != 'E'):
				cur_slot = getSlot(j)
				min_val = len(domain[i][j])
				min_i = i
				min_j = j
			elif(assignment[i][j] == None and len(domain[i][j]) == min_val and getSlot(j) == 'R' and cur_slot != 'M' and cur_slot != 'E' and cur_slot != 'R'):
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
	s = 'R'
	if(slot >= 0 and slot < m):
		s = 'M'
	elif(slot >= m and slot < m + a):
		s = 'A'
	elif(slot >= m + a and slot < m + a + e):
		s = 'E'

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

	if(isLastAssignment(assignment, day)):
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
	s = 'R'
	if(slot >= 0 and slot < m):
		s = 'M'
	elif(slot >= m and slot < m + a):
		s = 'A'
	elif(slot >= m + a and slot < m + a + e):
		s = 'E'

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
	new_domain = []
	s = 'R'
	if(slot >= 0 and slot < m):
		s = 'M'
	elif(slot >= m and slot < m + a):
		s = 'A'
	elif(slot >= m + a and slot < m + a + e):
		s = 'E'

	if(s != 'R'):
		return domain[day][slot]

	r_dict = {}
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
	for v in range(N):
		if(v in r_dict and v in domain[day][slot]):
			new_domain.append(v)
	return new_domain

def rosterSystem(assignment, domain):
	global calls
	calls += 1
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


result = rosterSystem(assignment, domain)
if(result == False):
	print("NO RESULT")
else:
	n_dict = {}
	for day in result:
		for slot in range(len(day)):
			s = 'R'
			if(slot >= 0 and slot < m):
				s = 'M'
			elif(slot >= m and slot < m + a):
				s = 'A'
			elif(slot >= m + a and slot < m + a + e):
				s = 'E'
			per = day[slot]
			if per in n_dict:
				n_dict[per].append(s)
			else:
				n_dict[per] = [s]
	for i in n_dict:
		print(i, n_dict[i])
print("Time: " + str(time.time() - start_time))
print("Calls: " + str(calls))