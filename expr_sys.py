import sys

def eval(expr, facts):
	lst = []
	c = 0
	par = 0
	pos = 0
	for elem in expr:
		if (elem.isspace()):
			c = c + 1
			continue
		if (elem == "("):
			par = par + 1
			pos = c
		elif (elem == ")"):
			par = par - 1
			lst.append(eval(expr[pos + 1:c], facts))
		elif (par == 0):
			lst.append(elem)
		c = c + 1
	pos = 0
	c = 0
	for elem in lst:
		if elem == "|":
			return "1" if (eval(lst[0:c], facts) == "1") or (eval(lst[c + 1:len(lst)], facts) == "1") else "0"
		c = c + 1
	c = 0
	for elem in lst:
		if (elem == "+"):
			return "1" if (eval(lst[0:c], facts) == "1") and (eval(lst[c + 1:len(lst)], facts) == "1") else "0"
		c = c + 1
	c = 0
	for elem in lst:
		if elem == "^":
			# print lst[0:c], "^",lst[c + 1:len(lst)]
			return "1" if (eval(lst[0:c], facts) == "1") ^ (eval(lst[c + 1:len(lst)], facts) == "1") else "0"
		c = c + 1
	if (lst[0] == "!"):
		if (lst[1] == "0"):
			return "1"
		for elem in facts:
			if (elem == lst[1]):
				return "0"
		return "1"
	if (lst[0] == "1"):
		return "1"
	if lst[0] in facts:
		return "1"
	return "0"

def query_analyse(query, rules, facts):
	ret = "none"
	if query in facts:
		print ('{:s} is True'.format(query))
		return "1"
	for rule in rules:
		members = rule.split("=>")
		if (len(members) < 2):
			print("error: syntax")
			exit()
		members[1] = members[1].strip()
		if query in members[1]:
			for sym in members[0]:
				if sym.isupper():
					if sym not in facts:
						if query_analyse(sym, rules, facts) == "1":
							facts.append(sym)
							print ('{:s} is True'.format(sym))
						else:
							print ('{:s} is False'.format(sym))
					else:
						print ('{:s} is True'.format(sym))
			print (rule),
			ret2 = eval(members[0], facts)
			if ret == "none" or ret == ret2:
				ret = ret2
			else:
				print "error: facts contradictoire"
				exit()
	return ret if ret == "0" or ret == "1" else "0"

if len(sys.argv) != 2:
	print "usage: ./expr_sys arg"
	exit()
in_file = open(sys.argv[1]);
mode = 0
rules = []
facts = []
queries = []
for line in in_file:
	lines = line.split("#")
	if len(lines[0]) == 0:
		continue
		lines[0] = lines[0].strip()
	if mode == 0:
		if line[0].startswith("="):
			mode = 1
		elif line[0].startswith("?"):
			mode = 2
		else :
			members = lines[0].split("=>")
			if (len(members) != 2):
				print("error: syntax")
				exit()
			for char in members[0]:
				if (not char.isupper() and char != '^' and char != '|' and char != '\t' and char != ' ' and char != '+' and char != '\n' and char != '!' and char != "(" and char != ")"):
					print "error: syntax"
					exit()
			for char in members[1]:
				if (not char.isupper()  and char != ' ' and char != '+' and char != '\n'):
					print "error: syntax"
					exit()
			rules.append(lines[0]);
	if mode == 1:
		if line[0].startswith("?"):
			mode = 2
		else:
			if (lines[0][0] != "="):
				print "error"
				exit()
			for fact in lines[0][1:len(lines[0]) - 1]:
				if (fact.isupper()):
					facts.append(fact)
				elif (fact != ' '):
					print "error: syntax"
					exit()
	if mode == 2:
		if (lines[0][0] != "?"):
			print "error"
			exit()
		for query in lines[0][1:len(lines[0])]:
			if (query.isupper()):
				queries.append(query)
			elif (query != ' '):
				print "error: syntax"
				exit()
for query in queries:
	print ('{:s}:'.format(query))
	if query_analyse(query, rules, facts) == "1":
		print ("So {:s} is True".format(query))
	else:
		print ("So {:s} is False".format(query))

in_file.close();