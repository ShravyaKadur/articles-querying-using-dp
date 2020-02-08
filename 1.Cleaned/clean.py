f1 = open('Articles.csv',mode='r', encoding='iso-8859-1')
f2 = open('ArticlesRefined.csv','w')
lines = f1.read().split('\n')
for line in lines:
	sub = ""
	for ch in line:
		if 32<=ord(ch)<=127:
			sub += ch
		else:
			chV = ord(ch)
			if chV==163:		#pound
				sub += ' (pounds) '
			elif chV==160:				#&nbsp for normal space
				sub += chr(32)
			elif chV==201:				#replacing special characters with plain characters
				sub += chr(ord('E'))
			elif chV==225 or chV==227:
				sub += chr(ord('a'))
			elif chV==231:
				sub += chr(ord('c'))
			elif chV==233:
				sub += chr(ord('e'))
			elif chV==237 or chV==239:
				sub += chr(ord('i'))
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
f1.close()
f2.close()
