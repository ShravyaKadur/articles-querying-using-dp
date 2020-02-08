import os
class Node:
	def display(self):
		pass

class SetN(Node):
	def __init__(self, val, cat):
		self.subsets = []
		self.setVal = val
		self.setCat = cat
	def display(self):
		for se in self.subsets:
			se.display()
	def addSubset(self, Subset):
		self.subsets.append(Subset)
	def getChildren(self):
		return self.subsets[:]
	def getArticles(self):
		li = []
		for se in self.subsets:
			if type(se).__name__=='SetN':
				li.extend(se.getArticles())
			else:
				li.append(se)
		return list(set(li))

class ArtN(Node):
	def __init__(self, no):
		self.artNo = no
	def display(self):
		i = 1
		f = open("ArticlesFinal.csv","r")
		line = f.readline()
		colNos = len(line.split(','))
		while line:
			line = f.readline().rsplit(',',colNos-1)
			if i==self.artNo:
				print(line[2],'\n',line[1])
				print(line[0])
				print('<press any key to continue>')
				input()
#				print(chr(27)+"[2J")
				os.system('cls' if os.name == 'nt' else 'clear')
#				print('--------------------------------------------------------------------------')
				break
			i += 1
		

def build_tree(root, tree, emptyLabel):
	for k,v in tree.items():
		if type(v).__name__ == 'dict':
			k1,k2 = k.split(';')
			child = SetN(k1, k2)
			build_tree(child, v, emptyLabel)
			root.addSubset(child)
		elif type(v).__name__ == 'list':
			if k==emptyLabel:
				for node in v:
					root.addSubset(node)
			else:
				k1,k2 = k.split(';')
				child = SetN(k1, k2)
				root.addSubset(child)
				for node in v:
					child.addSubset(node)
				

def allKeys(di):
	lo = list(di.keys())
	for k in di.keys():
		if type(di[k]).__name__=='dict':
			lo.extend(allKeys(di[k]))
	return lo

def create_initial_tree():
	f = open("ArticlesFinal.csv","r")
	line = f.readline()
	colNos = len(line.split(','))

	i = 1
	emptyLabel = '<EMPTY FIELD IN DATA>'
	tree = {}
	while line:
		line = f.readline()
		if line!='':
			line = line.rsplit(',',colNos-1)
			art = ArtN(i)
			if line[3]!='':
				line[3] = line[3].lower().strip()+";sport"
				if not line[3] in tree.keys():
					tree[line[3]] = {}
				
				if line[4]!='':
					line[4] = line[4].lower().strip()+";location"
					if not line[4] in tree[line[3]].keys():
						tree[line[3]][line[4]] = {}

					if line[5]!='' or line[6]!='':
						line[5] = line[5].lower()
						line[6] = line[6].lower()
						names = ''
						if line[5]=='':
							names = line[6]
						elif line[6]=='':
							names = line[5]
						else:
							names = line[5]+';'+line[6]
						names = names.split(';')
						orgs = False
						if line[7]!='' and line[7]!='\n':
							line[7] = line[7].lower()
							orgs = line[7].split(';')
						for name in names:
							name = name.strip()+";person"
							if not name in tree[line[3]][line[4]].keys():
								tree[line[3]][line[4]][name] = {}
							if orgs:
								for org in orgs:
									org = org.strip()+";organisation"
									if not org in tree[line[3]][line[4]][name].keys():
										tree[line[3]][line[4]][name][org] = []
									tree[line[3]][line[4]][name][org].append(art)
								
							else:
								if not emptyLabel in tree[line[3]][line[4]][name].keys():
									tree[line[3]][line[4]][name][emptyLabel] = []
								tree[line[3]][line[4]][name][emptyLabel].append(art)
					elif line[7]!='' and line[7]!='\n':
						line[7] = line[7].lower()
						orgs = line[7].split(';')
						for org in orgs:
							org = org.strip()+";organisation"
							if not org in tree[line[3]][line[4]].keys():
								tree[line[3]][line[4]][org] = []
							tree[line[3]][line[4]][org].append(art)
					else:
						if not emptyLabel in tree[line[3]][line[4]].keys():
							tree[line[3]][line[4]][emptyLabel] = []
						tree[line[3]][line[4]][emptyLabel].append(art)

				elif line[5]!='' or line[6]!='':
					line[5] = line[5].lower()
					line[6] = line[6].lower()
					names = ''
					if line[5]=='':
						names = line[6]
					elif line[6]=='':
						names = line[5]
					else:
						names = line[5]+';'+line[6]
					names = names.split(';')
					orgs = False
					if line[7]!='' and line[7]!='\n':
						line[7] = line[7].lower()
						orgs = line[7].split(';')
					for name in names:
						name = name.strip()+";person"
						if not name in tree[line[3]].keys():
							tree[line[3]][name] = {}
						if orgs:
							for org in orgs:
								org = org.strip()+";organisation"
								if not org in tree[line[3]][name].keys():
									tree[line[3]][name][org] = []
								tree[line[3]][name][org].append(art)
							
						else:
							if not emptyLabel in tree[line[3]][name].keys():
								tree[line[3]][name][emptyLabel] = []
							tree[line[3]][name][emptyLabel].append(art)
				elif line[7]!='' and line[7]!='\n':
					line[7] = line[7].lower()
					orgs = line[7].split(';')
					for org in orgs:
						org = org.strip()+";organisation"
						if not org in tree[line[3]].keys():
							tree[line[3]][org] = []
						tree[line[3]][org].append(art)
				else:
					if not emptyLabel in tree[line[3]].keys():
						tree[line[3]][emptyLabel] = []
					tree[line[3]][emptyLabel].append(art)
			elif line[4]!='':
				line[4] = line[4].lower().strip()+";location"
				if not line[4] in tree.keys():
					tree[line[4]] = {}

				if line[5]!='' or line[6]!='':
					line[5] = line[5].lower()
					line[6] = line[6].lower()
					names = ''
					if line[5]=='':
						names = line[6]
					elif line[6]=='':
						names = line[5]
					else:
						names = line[5]+';'+line[6]
					names = names.split(';')
					orgs = False
					if line[7]!='' and line[7]!='\n':
						line[7] = line[7].lower()
						orgs = line[7].split(';')
					for name in names:
						name = name.strip()+";person"
						if not name in tree[line[4]].keys():
							tree[line[4]][name] = {}
						if orgs:
							for org in orgs:
								org = org.strip()+";organisation"
								if not org in tree[line[4]][name].keys():
									tree[line[4]][name][org] = []
								tree[line[4]][name][org].append(art)
							
						else:
							if not emptyLabel in tree[line[4]][name].keys():
								tree[line[4]][name][emptyLabel] = []
							tree[line[4]][name][emptyLabel].append(art)
				elif line[7]!='' and line[7]!='\n':
					line[7] = line[7].lower()
					orgs = line[7].split(';')
					for org in orgs:
						org = org.strip()+";organisation"
						if not org in tree[line[4]].keys():
							tree[line[4]][org] = []
						tree[line[4]][org].append(art)
				else:
					if not emptyLabel in tree[line[4]].keys():
						tree[line[4]][emptyLabel] = []
					tree[line[4]][emptyLabel].append(art)

			elif line[5]!='' or line[6]!='':
				line[5] = line[5].lower()
				line[6] = line[6].lower()
				names = ''
				if line[5]=='':
					names = line[6]
				elif line[6]=='':
					names = line[5]
				else:
					names = line[5]+';'+line[6]
				names = names.split(';')
				orgs = False
				if line[7]!='' and line[7]!='\n':
					line[7] = line[7].lower()
					orgs = line[7].split(';')
				for name in names:
					name = name.strip()+";person"
					if not name in tree.keys():
						tree[name] = {}
					if orgs:
						for org in orgs:
							org = org.strip()+";organisation"
							if not org in tree[name].keys():
								tree[name][org] = []
							tree[name][org].append(art)
						
					else:
						if not emptyLabel in tree[name].keys():
							tree[name][emptyLabel] = []
						tree[name][emptyLabel].append(art)
			elif line[7]!='' and line[7]!='\n':
				line[7] = line[7].lower()
				orgs = line[7].split(';')
				for org in orgs:
					org = org.strip()+";organisation"
					if not org in tree.keys():
						tree[org] = []
					tree[org].append(art)

			else:
				if not emptyLabel in tree.keys():
					tree[emptyLabel] = []
				tree[emptyLabel].append(art)
			i += 1
	f.close()
#	print(tree)
	print(tree['squash;sport']['paris;location'])
	lookup = allKeys(tree)
	lookup = set(lookup)
#	print(lookup)
	root = SetN('root','root')
	build_tree(root,tree,emptyLabel)
	return root,lookup


'''
root = SetN('root','root')
cri = SetN('cricket','sport')
ot = SetN('other','sport')
f = open("ArticlesFinal.csv","r")
i = 1
line = f.readline()
while line and i<=40:
	line = f.readline()
	line = line.split(',')[-5]
	if line=='cricket':
		cri.addSubset(ArtN(i))
	else:
		ot.addSubset(ArtN(i))
	i += 1
root.addSubset(cri)
root.addSubset(ot)

print("ON A NON-LEAF NODE:")
print("CLASS NAME: ",type(ot).__name__)
ot.display()
print("CALLING ON A LEAF NODE:")
print("CLASS NAME: ",type(ot.getChildren()[0]).__name__)
ot.getChildren()[0].display()
'''
root,lookup=create_initial_tree()
print(len(root.getArticles()))

def dfs(node, I):
	ch = node.getChildren()
	for c in ch:
		if type(c).__name__=='ArtN':
			print(c.artNo,I)
	for c in ch:
		if type(c).__name__=='SetN':
			print(c.setVal,I)
			input()
			dfs(c,I+1)

#dfs(root,0)
'''
s = root.getChildren()
ss = []
for k in s:
	if type(k).__name__=='SetN' and k.setVal=='tennis':
		ss.extend(k.getChildren())
for s in ss:
	print(s.setCat)'''
