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
		if (elem == "+"):
			return "1" if (eval(lst[0:c], facts) == "1") and (eval(lst[c + 1:len(lst)], facts) == "1") else "0"
		c = c + 1
	c = 0
	for elem in lst:
		if elem == "|":
			return "1" if (eval(lst[0:c], facts) == "1") or (eval(lst[c + 1:len(lst)], facts) == "1") else "0"
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
	for elem in facts:
		if (elem == lst[0]):
			return "1"
	return "0"

in_file = open("test");
mode = 0
rules = []
facts = []
queries = []
for line in in_file:
	lines = line.split("#")
	if len(lines[0]) == 0:
		continue
	if mode == 0:
		if line[0].startswith("="):
			mode = 1
		elif line[0].startswith("?"):
			mode = 2
		else :
			rules.append(lines[0]);
	if mode == 1:
		if line[0].startswith("?"):
			mode = 2
		else:
			for fact in lines[0][1:len(lines[0])]:
				if (fact.isupper()):
					facts.append(fact)
	if mode == 2:
		for query in lines[0][1:len(lines[0])]:
			if (query.isupper()):
				queries.append(query)
print rules
print facts
print queries
for rule in rules:
	members = rule.split("=>")
	members[1] = members[1].strip()
	if (len(members[1]) > 0):
		ret = eval(members[0], facts)
		print members[0] , "->" , ret
	else :
		print "error"
		exit()
in_file.close();