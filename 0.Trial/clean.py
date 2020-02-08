f1 = open('Articles.csv',mode='r', encoding='iso-8859-1')
f2 = open('ArticlesRefined.csv','w')
lines = f1.read().split('\n')
for line in lines:
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
f1.close()
f2.close()
