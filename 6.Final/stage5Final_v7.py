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
		self.visited = 0
	def display(self):
		li = self.getArticles()
		for se in li:
			se.display()
	def addSubset(self, Subset):
		assert issubclass(Subset.__class__,Node), 'Unacceptable Subset'
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
	def setZeroes(self):
		self.visited = 0
		for se in self.subsets:
			if type(se).__name__=='SetN':
				se.setZeroes()

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
				print('<press enter to continue>')
				input()
				os.system('clear')
				break
			i += 1
		

class Iterator:
	def __init__(self, tree, val, cat):
		self.root = tree.root
		self.root.setZeroes()
		self.find(val, cat)
	
	def __iter__(self):
		return self
	
	def getNeighbour(self, node):
		if node==None:
			return node
		parent = node.parent
		if parent==None:
			return parent
		curr = parent.getChildren().index(node)
		if curr<len(parent.getChildren())-1:
			return parent.getChildren()[curr+1]
		else:
			if(self.getNeighbour(parent)):
				if type(self.getNeighbour(parent)).__name__=='SetN':
					if(self.getNeighbour(parent).getChildren):
						return self.getNeighbour(parent).getChildren()[0]
					else:
						return None
				else:
					return None
			else:
				return None
	
	def __next__(self, node):
		for child in node.getChildren():
			if type(child).__name__=='SetN' and child.visited==0:
				return child
	
	def find(self, val, cat):
		self.newRoot = SetN(val, cat)
		
		def dfs(node):
			if node.setCat==cat and node.setVal==val:
				for ch in node.getChildren():
					self.newRoot.addSubset(ch)
			
			else:
				nextNode = self.__next__(node)
				while(nextNode):
					nextNode.visited = 1
					dfs(nextNode)
					nextNode = self.__next__(node)
		
		dfs(self.root)
		
		return self.newRoot
		
	
class QueryStrategy:
	def getQueryFn(self, queryStr):
		obj = None
		if '|' in queryStr:
			if '&' in queryStr:
				obj = QueryAndOr()
			else:
				obj = QueryOr()
		elif '&' in queryStr:
			obj = QueryAnd()
		else:
			obj = QuerySimple()
		return obj
class QueryAnd(QueryStrategy):
	def query(self, tree, queryStr):
		queryStr = queryStr.lower()
		setList = []
		strs = queryStr.split('&')
		strs = [s.strip() for s in strs]
		result = SetN('reroot', 'reroot')
		for str in strs:
			cat = tree.checkLookup(str)
			iter = Iterator(tree, str, cat)
			result.addSubset(iter.newRoot)
			setList.append(set(iter.newRoot.getArticles()))
		attrSet = setList[0]
		for s in setList:
			attrSet &= s
		result = tree.pruneTree(result, attrSet)
		return Tree(result, tree.lookup)
	
class QueryOr(QueryStrategy):
	def query(self, tree, queryStr):
		queryStr = queryStr.lower()
		strs = queryStr.split('|')
		strs = [s.strip() for s in strs]
		result = SetN('reroot', 'reroot')
		for str in strs:
			cat = tree.checkLookup(str)
			iter = Iterator(tree, str, cat)
			result.addSubset(iter.newRoot)
		return Tree(result, tree.lookup)
	
class QueryAndOr(QueryStrategy):
	def query(self, tree, queryStr):
		queryStr = queryStr.lower()
		subquery = queryStr.split('|')
		subquery = [s.strip() for s in subquery]
		result = SetN('reroot', 'reroot')
		for quer in subquery:
			if '&' in quer:
				setList = []
				strs = quer.split('&')
				strs = [s.strip() for s in strs]
				subResult = SetN('reroot', 'reroot')
				for str in strs:
					cat = tree.checkLookup(str)
					iter = Iterator(tree, str, cat)
					subResult.addSubset(iter.newRoot)
					setList.append(set(iter.newRoot.getArticles()))
				attrSet = setList[0]
				for s in setList:
					attrSet &= s
				subResult = tree.pruneTree(subResult, attrSet)
				result.addSubset(subResult)
			else:
				quer = quer.strip()
				cat = tree.checkLookup(quer)
				subResult = SetN('reroot', 'reroot')
				iter = Iterator(tree, quer, cat)
				subResult.addSubset(iter.newRoot)
				result.addSubset(subResult)
		return Tree(result, tree.lookup)


class QuerySimple(QueryStrategy):
	def query(self, tree, queryStr):
		queryStr = queryStr.lower()
		queryStr = queryStr.strip()
		cat = tree.checkLookup(queryStr)
		result = SetN('reroot', 'reroot')
		iter = Iterator(tree, queryStr, cat)
		result.addSubset(iter.newRoot)
		return Tree(result, tree.lookup)
			
class Tree():
	def build_tree(self,root, tree, emptyLabel):
		for k,v in sorted(tree.items(), key = lambda a: a[0]):
			if type(v).__name__ == 'dict':
				k1,k2 = k.split(';')
				child = SetN(k1, k2)
				self.build_tree(child, v, emptyLabel)
				root.addSubset(child)
				child.setParent(root)
			elif type(v).__name__ == 'list':
				l1 = len(v)
				vCopy = list(set(v))
				l2 = len(vCopy)
				if l1!=l2:
					print("REPETITION")
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
				

	def allKeys(self,di):
		lo = list(di.keys())
		for k in di.keys():
			if type(di[k]).__name__=='dict':
				lo.extend(self.allKeys(di[k]))
		return lo

	def create_initial_tree(self):
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
								names = line[5].strip()+';'+line[6].strip()
							names = names.split(';')
							for loop in range(len(names)):
								names[loop] = names[loop].strip()
							names = list(sorted(set(names), key=names.index))
							orgs = False
							if line[7]!='' and line[7]!='\n' and line[7]!='\r':
								line[7] = line[7].lower()
								orgs = line[7].split(';')
								for loop in range(len(orgs)):
									orgs[loop] = orgs[loop].strip()
								orgs = list(sorted(set(orgs), key=orgs.index))
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
						elif line[7]!='' and line[7]!='\n' and line[7]!='\r':
							line[7] = line[7].lower()
							orgs = line[7].split(';')
							for loop in range(len(orgs)):
								orgs[loop] = orgs[loop].strip()
							orgs = list(sorted(set(orgs), key=orgs.index))
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
						for loop in range(len(names)):
							names[loop] = names[loop].strip()
						names = list(sorted(set(names), key=names.index))
						orgs = False
						if line[7]!='' and line[7]!='\n':
							line[7] = line[7].lower()
							orgs = line[7].split(';')
							for loop in range(len(orgs)):
								orgs[loop] = orgs[loop].strip()
							orgs = list(sorted(set(orgs), key=orgs.index))
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
						for loop in range(len(orgs)):
							orgs[loop] = orgs[loop].strip()
						orgs = list(sorted(set(orgs), key=orgs.index))
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
						for loop in range(len(names)):
							names[loop] = names[loop].strip()
						names = list(sorted(set(names), key=names.index))
						orgs = False
						if line[7]!='' and line[7]!='\n':
							line[7] = line[7].lower()

							orgs = line[7].split(';')
							for loop in range(len(orgs)):
								orgs[loop] = orgs[loop].strip()
							orgs = list(sorted(set(orgs), key=orgs.index))
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
						for loop in range(len(orgs)):
							orgs[loop] = orgs[loop].strip()
						orgs = list(sorted(set(orgs), key=orgs.index))
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
					for loop in range(len(names)):
						names[loop] = names[loop].strip()
					names = list(sorted(set(names), key=names.index))
					orgs = False
					if line[7]!='' and line[7]!='\n':
						line[7] = line[7].lower()
						orgs = line[7].split(';')
						for loop in range(len(orgs)):
							orgs[loop] = orgs[loop].strip()
						orgs = list(sorted(set(orgs), key=orgs.index))
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
					for loop in range(len(orgs)):
						orgs[loop] = orgs[loop].strip()
					orgs = list(sorted(set(orgs), key=orgs.index))
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
		lookup = self.allKeys(tree)
		lookup = set(lookup)
		root = SetN('root','root')
		self.build_tree(root,tree,emptyLabel)
		return root,lookup
	def __init__(self, root = None, lookup = None):
		assert bool(root)==bool(lookup), 'Must create tree with lookup only'
		if not root:
			root,lookup=self.create_initial_tree()
		self.root = root
		self.lookup = lookup
		self.querSys = QueryStrategy()
	def checkLookup(self, key):
		cats = ['sport','location','organisation','person']
		for c in cats:
			if key+';'+c in self.lookup:
				return c
		return 'invalid'
	def dfsDict(self, root, aSet, valList, newTreeDict, emptyLabel):
		if type(root).__name__=='SetN':
			if root.setVal!='reroot':
				k = root.setVal+';'+root.setCat
				valList.append(k)
			for x in root.getChildren():
				self.dfsDict(x, aSet, valList[:], newTreeDict, emptyLabel)
		else:
			if root in aSet:
				k = newTreeDict
				for x in valList:
					if x not in k.keys():
						k[x] = {}
					k = k[x]
				if emptyLabel not in k.keys():
					k[emptyLabel] = []
				k[emptyLabel].append(root)

	def pruneTree(self,root, aSet):
		emptyLabel = "<EMPTY LABEL>"
		newTreeRoot = {}
		self.dfsDict(root, aSet, [], newTreeRoot, emptyLabel)
		reroot = SetN('reroot','reroot')
		self.build_tree(reroot, newTreeRoot, emptyLabel)
		return reroot
	def runQuery(self):
		cont = True
		while cont:
			print('Please enter a query with any of the following separated by & and/or |: sportnames, sportpersons, locations, ')
			queryStr = input()
			while queryStr=='':
				print("Empty query. Try again? (Y/N)")
				a = input()
				if a=='N':
					cont = False
					break
				else:
					queryStr = input()
			
			if queryStr!='':
				queryObj = self.querSys.getQueryFn(queryStr)
				finalTree = queryObj.query(self,queryStr)
				finalTree.root.display()
				if len(finalTree.root.getArticles())==0:
					print("\nYour query did not return any results.")
				print("Run another query? (Y/N)")
				a = input()
				if a=='N':
					cont = False
				
				
tree = Tree()
print('Tree Construction Done. Continue?')
input()
tree.runQuery()
