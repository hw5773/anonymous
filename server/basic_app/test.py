import os
import sys

java_files = []				# the list of java files
rel_set = []				# the relation list
instance_to_class = {}		# the mapping between instance and class
curr_class = ""				# the name of the current class

def parsing(blk, cname, fname):
	c = ""
	l = ""
	i = 0

	skip = False
	comment = False

	while len(blk) > 0:
		c = blk[0]
		blk = blk[1:]

		if skip:
			if c == "\n":
				skip = False
			continue
		elif comment:
			if blk[0:1] == "*/":
				comment = False
			continue
		else:
			if c == "@" or (c == "/" and blk[0] == "/"):
				skip = True
				l = ""
				continue
			elif c == "/" and blk[0] == "*":
				comment = True
				l = ""
				continue
#			elif c == "(":
#				stack = [1]
#				b = c
#				while len(stack) > 0:
#					c = blk[0]
#					blk = blk[1:]
#					b = b + c
#					if c == "(":
#						stack.append(1)
#					elif c == ")":
#						stack.pop()
					
#					if len(stack) == 0:
#						c = b
			elif c == "\n" or c == "\r":
				continue
			elif c == ";":
				print l.strip()
				l = ""
				continue
			elif c == "{":
				stack = [1]
				b = ""
				print "line: %s" % l.strip()
				print "block start"
				while len(stack) > 0:
					c = blk[0]
					blk = blk[1:]
					if c == "{":
						stack.append(1)
					elif c == "}":
						stack.pop()

					if len(stack) > 0:
						b = b + c
				parsing(b, l, l)
				print "block end"
				continue

			l = l + c

for root, dirs, files in os.walk("."):
	for f in files:
		if ".java" in f:
			java_files.append(f)

print "java_files: "
print java_files

l = ""

java_files = ["HttpUtil.java"]

for f in java_files:
	fi = open(f, "r")
	l = fi.read()

	print fi
	parsing(l, "", "")
	print "\n"
