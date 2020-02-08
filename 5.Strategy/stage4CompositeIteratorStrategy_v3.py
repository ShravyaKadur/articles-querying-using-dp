import os
class Node:
	parent = None
	def setParent(self, parent):
		self.parent = parent
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
				os.system('clear')
				break
			i += 1
		

def build_tree(root, tree, emptyLabel):
	for k,v in tree.items():
		if type(v).__name__ == 'dict':
			k1,k2 = k.split(';')
			child = SetN(k1, k2)
			build_tree(child, v, emptyLabel)
			root.addSubset(child)
			child.setParent(root)
		elif type(v).__name__ == 'list':
			if k==emptyLabel:
				for node in v:
					root.addSubset(node)
					node.setParent(root)
			else:
				k1,k2 = k.split(';')
				child = SetN(k1, k2)
				root.addSubset(child)
				child.setParent(root)
				for node in v:
					child.addSubset(node)
					node.setParent(child)
				

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
#	print(tree['squash;sport']['paris;location'])
	lookup = allKeys(tree)
	lookup = set(lookup)
	root = SetN('root','root')
	build_tree(root,tree,emptyLabel)
	return root,lookup


class Iterator:

	root = SetN('root', 'root')
	
	def __init__(self, root, val, cat):
		self.root = root
		self.find(val, cat)
	
	def __iter__(self):
		return self
	
	def __next__(self, node):
		if node==None:
			return node
		parent = node.parent
		if parent==None:
			return parent
		curr = parent.subsets.index(node)
		if curr<len(parent.subsets)-1:#(parent.subsets[curr+1]):(changed)
			return parent.subsets[curr+1]
		else:
			if(self.__next__(parent)):
				if type(self.__next__(parent)).__name__=='SetN':
					if(self.__next__(parent).getChildren):				#'ArtN' object has no attribute 'getChildren'
						return self.__next__(parent).getChildren()[0]
					else:
						return None
				else:
					return None
			else:
				return None
	
	def find(self, val, cat):
		self.newRoot = SetN(val, cat)

		initial = self.root.subsets[0]
		isInitSet = type(initial).__name__=='SetN'
		curr = initial
		
		while(initial):
			if type(curr).__name__=='SetN':
				if(isInitSet==False):
					initial = curr
					isInitSet = True
				
				if curr.setCat==cat:
					if curr.setVal==val:
						self.newRoot.addSubset(curr.subsets)
				else:
					initial = initial.subsets[0]					#'ArtN' object has no attribute 'subsets'
					isInitSet = type(initial).__name__=='SetN'
					curr = initial
			curr = self.__next__(curr)
			if curr==None and isInitSet==False:
				break
		
		return self.newRoot


class QueryStrategy:
	def __init__(self, lookup):
		self.lookup = lookup
	def checkLookup(self, key):			#returns which category a simple query belongs to
		cats = ['sport','location','organisation','person']
		for c in cats:
			if key+';'+c in self.lookup:
				return c
		return 'invalid'		#should not reach here
	def getQueryFn(self, queryStr):
	
		def queryAnd(self, queryStr):
			strs = queryStr.split('&')	#strip
			result = SetN('reroot', 'reroot')
			otree = self.root
			catdict = {'sport':0,'location':1,'organisation':2,'person':3}
			strs.sort(key=lambda str: catdict[self.checkLookup(str)])
			for str in strs:
				cat = self.checkLookup(str)
				iter = Iterator(otree, str, cat)
				result.addSubset(iter.newRoot)
				otree = iter.newRoot
			return result
		
		def queryOr(self, queryStr):
			strs = queryStr.split('|')
			result = SetN('reroot', 'reroot')
			for str in strs:
				cat = self.checkLookup(str)
				iter = Iterator(self.root, str, cat)
				result.addSubset(iter.newRoot)
			return result
		
		def queryAndOr(self, queryStr):
			pass
		
		def querySimple(self, queryStr):
			print(type(self))
			cat = self.querSys.checkLookup(queryStr)
			result = SetN('reroot', 'reroot')
			iter = Iterator(self.root, queryStr, cat)
			result.addSubset(iter.newRoot)
			return result

		if '|' in queryStr:
			if '&' in queryStr:
				return queryAndOr
			else:
				return queryOr
		elif '&' in queryStr:
			return queryAnd
		else:
			return querySimple
			
class Tree():
	def __init__(self):
		root,lookup=create_initial_tree()
		self.root = root
		self.querSys = QueryStrategy(lookup)
	def query(self, queryStr):
		pass
	def runQuery(self):
		cont = True
		while cont:
			print('Please enter a query with any of the following separated by & and/or |: sportnames, sportpersons, locations, ')
			queryStr = input()
			self.query = self.querSys.getQueryFn(queryStr)
			
			#run query, get tree, do something :P
			finalTree = self.query(self, queryStr)
			
			#Print tree code goes here
			
			os.system('clear')
			print("Run another query? (Y/N)")
			a = input()
			os.system('clear')
			if a=='N':
				cont = False
				
				
tree = Tree()
tree.runQuery()
