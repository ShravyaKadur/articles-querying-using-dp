from __future__ import print_function
import sys

def eprint(*args, **kwargs):			#write to stderr
	print(*args, file=sys.stderr, **kwargs)

weird_characters = []

f1 = open('Articles.csv',mode='r', encoding='iso-8859-1')
f2 = open('ArticlesRefinedTestOddChar.csv','w')
lines = f1.read().split('\n')
lineNo = 0
for line in lines:
	lineNo += 1
	sub = ""
	letterNo = 0
	for ch in line:
		letterNo += 1
		if 32<=ord(ch)<=127:
			sub += ch
		else:
			weird_characters.append(ord(ch))
			eprint(lineNo,':',letterNo,' ---HAD--- ',ch,":",ord(ch))
	line = sub
	if line[:7]=='strong>':
		line = line[7:]
		ind = line.index('</strong')
		line = line[:ind] + line[ind+8:]
	elif line[:8]=='"strong>':
		line = line[8:]
		ind = line.index('</strong')
		line = '"' + line[:ind] + line[ind+8:]
	f2.write(line)
	f2.write('\n')
weird_characters = sorted(list(set(weird_characters)))
weird_list = [hex(x)+':'+str(x) for x in weird_characters]
eprint(weird_list)
f1.close()
f2.close()
