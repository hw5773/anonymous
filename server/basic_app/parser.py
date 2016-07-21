import os
import sys

java_files = []				# the list of java files
rel_set = []				# the relation list
curr_class = ""				# the name of the current class

keywords = ["try", "catch", "while"]
types = ["String", "int", "float", "double"]

def parse_left(left):
	left_lst = left.strip().split(" ")
	var = left_lst[-1]

	if len(left_lst) == 2:
		pre = left_lst[0].strip()
		if pre not in types:
			instance_to_class[var] = pre
	elif len(left_lst) > 2:
		print "more than 2: %s" % left
	
	return var	

def parse_right(var, right):
	s1 = set([])
	s1.add(var)
	if "new" in right:
		idx = right.index("new")
		num = idx + 3
		val = right[num:num+right[num:].index("(")].strip()
		instance_to_class[var] = val
		s1.add(val)
		
	elif right[0] == "(":
		val = right[right.index(")")+1:].strip()
		s1.add(val)

		try:
			idx1 = val.index("(")
		except:
			idx1 = -1

		if idx1 > 0:
			try:
				idx2 = val.index(")")
			except:
				idx2 = -1
			if idx2 > 0:
				val = val[idx1+1:idx2]
				s1.add(val)

	add_rel(s1)

def parse_line(line, cname, fname):
	line = line.strip()

	if "=" in line:
		idx = line.index("=")
		left = line[0:idx].strip()
		var = parse_left(left)
		right = line[idx+1:].strip()
		parse_right(var, right)

	if "return" in line:
		idx = line.index(" ")
		val = line[idx+1:]
		s1 = set([])
		s1.add(fname)
		s1.add(val)
		add_rel(s1)
		
def add_rel(s1):
	contain = False
	for elem in rel_set:
		s2 = set(elem)

		if s1 & s2:
			contain = True
			rel_set.remove(elem)
			rel_set.append(list(s1 | s2))

	if not contain:
		if list(s1):
			rel_set.append(list(s1))

def parsing(blk, cname, fname, ref_to_class, inst_to_class):
	c = "" 			# current character
	l = "" 			# current line
	i = 0  			# counter

	skip = False	#
	comment = False	#
	in_str = False	#

	while len(blk) > 0:
		c = blk[0]
		blk = blk[1:]

		if skip:
			if c == "\n":												# 줄변환 무시
				skip = False
			continue
		elif comment:
			if c == "*" and blk[0] == "/":								# 주석 무시
				comment = False
				blk = blk[1:]
			continue
		else:
			if c == "@":												# annotation 무시
				skip = True
				l = ""
				continue
			elif c == "\"":												# string 내의 URL 때문에
				if in_str == True:
					in_str = False
				else:
					in_str = True
			elif c == "/" and blk[0] == "/" and not (in_str == True):	# 주석 무시
				skip = True
				l = ""
				blk = blk[1:]
				continue
			elif c == "/" and blk[0] == "*":							# 주석 무시
				comment = True
				blk = blk[1:]
				l = ""
				continue
			elif c == "\n" or c == "\r":
				continue
			elif c == ";":
				print l.strip()
				parse_line(l, cname, fname)
				l = ""
				continue
			elif c == "{":
				stack = [1]
				b = ""
				l = l.strip()

				while len(stack) > 0:
					c = blk[0]
					blk = blk[1:]
					if c == "{":
						stack.append(1)
					elif c == "}":
						stack.pop()

					if len(stack) > 0:
						b = b + c

				if "class" in l:
					class_name = parse_class(l)
					parsing(b, class_name, fname, ref_to_class, inst_to_class)
				elif "for" in l:
					# parse for "for"
				elif ("if" or "else") in l:
					# parse for "if-else"
				elif ("switch") in l:
					# parse for "switch"

				else:
					ret = parse_func(l)
					r2c = dict(ref_to_class)
					for k in ret["r2c"].keys():
						r2c[k] = ret["r2c"][k]
						
					parsing(b, cname, ret["func_name"], r2c, inst_to_class)

				l = ""
				print "block end"
				continue

			l = l + c

def parse_class(prefix):
	lst = prefix.split(" ")
	idx = lst.index("class")
	idx = idx + 1
	return lst[idx]

def parse_func(prefix):
	idx = 1
	ret = {}
	ret["func_name"] = ""
	ret["r2c"] = {}
	
	while idx > 0:
		try:
			idx = prefix.index(" ")
			idx2 = prefix.index("(")
			if idx < idx2:
				prefix = prefix[idx+1:]
		except:
			idx = -1
			idx2 = prefix.index("(")
			ret["func_name"] = prefix[0:idx2]

	idx1 = prefix.index("(")
	idx2 = prefix.index(")")
	params = prefix[idx1+1:idx2]

	ret["r2c"] = parse_params(params)

	return ret

def parse_params(params):
	lst = params.split(",")
	r2c = {}
	for p in lst:
		idx = p.strip().index(" ")
		c = p[0:idx].strip()
		r = p[idx+1:].strip()
		r2c[r] = c

	return r2c

for root, dirs, files in os.walk("."):
	for f in files:
		if ".java" in f:
			java_files.append(f)

print "java_files: "
print java_files

#java_files = ["GpsInfo.java"]

for f in java_files:
	fi = open(f, "r")
	b = fi.read()

	print fi
	parsing(b, "", "", {}, {})
	print "\n"

print "rel_set: "
for s in rel_set:
	print s

