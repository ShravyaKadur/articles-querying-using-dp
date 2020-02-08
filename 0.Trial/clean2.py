import re
f1 = open('ArticlesRefined.csv',mode='r', encoding='iso-8859-1')
f2 = open('ArticlesRefined2.csv','w')
lines = f1.read().split('\n')
for line in lines:
	l = re.split('<.*>',line)
	print(l)
	line = ""
	for li in l:
		line = line + li
	f2.write(line)
	f2.write('\n')
f1.close()
f2.close()
