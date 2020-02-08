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
		li = self.getArticles()
		for se in li:
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
				print('<press enter to continue>')
				input()
				os.system('clear')
				break
			i += 1
		

def build_tree(root, tree, emptyLabel):
	for k,v in sorted(tree.items(), key = lambda a: a[0]):
		if type(v).__name__ == 'dict':
			k1,k2 = k.split(';')
			child = SetN(k1, k2)
			build_tree(child, v, emptyLabel)
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
		curr = parent.getChildren().index(node)
		if curr<len(parent.getChildren())-1:
			return parent.getChildren()[curr+1]
		else:
			if(self.__next__(parent)):
				if type(self.__next__(parent)).__name__=='SetN':
					if(self.__next__(parent).getChildren):
						return self.__next__(parent).getChildren()[0]
					else:
						return None
				else:
					return None
			else:
				return None
	
	def find(self, val, cat):
		self.newRoot = SetN(val, cat)

		initial = self.root.getChildren()[0]
		isInitSet = type(initial).__name__=='SetN'
		curr = initial
		
		while(initial):
			if type(curr).__name__=='SetN':
				if(isInitSet==False):
					initial = curr
					isInitSet = True
				
				if curr.setCat==cat:
					if curr.setVal==val:
						for ch in curr.getChildren():
							self.newRoot.addSubset(ch)
			if not curr:
				initial = initial.getChildren()[0]
				isInitSet = type(initial).__name__=='SetN'
				curr = initial
			curr = self.__next__(curr)
			if curr==None and isInitSet==False:
				break
		
		return self.newRoot


class QueryStrategy:
	def __init__(self, lookup):
		self.lookup = lookup
	def checkLookup(self, key):
		cats = ['sport','location','organisation','person']
		for c in cats:
			if key+';'+c in self.lookup:
				return c
		return 'invalid'
	def getQueryFn(self, queryStr):
	
		def queryAnd(self, queryStr):
			strs = queryStr.split('&')
			strs = [s.strip() for s in strs]
			result = SetN('reroot', 'reroot')
			otree = self.root
			catdict = {'sport':0,'location':1,'person':2,'organisation':3}
			strs.sort(key=lambda str: catdict[self.checkLookup(str)])
			for str in strs:
				cat = self.checkLookup(str)
				iter = Iterator(otree, str, cat)
				otree = iter.newRoot
			result.addSubset(otree)
			return result
		
		def queryOr(self, queryStr):
			strs = queryStr.split('|')
			strs = [s.strip() for s in strs]
			result = SetN('reroot', 'reroot')
			for str in strs:
				cat = self.checkLookup(str)
				iter = Iterator(self.root, str, cat)
				result.addSubset(iter.newRoot)
			return result
		
		def queryAndOr(self, queryStr):
			subquery = queryStr.split('|')
			subquery = [s.strip() for s in subquery]
			result = SetN('reroot', 'reroot')
			for quer in subquery:
				if '&' in quer:
					strs = quer.split('&')	#strip
					strs = [s.strip() for s in strs]
					subResult = SetN('reroot', 'reroot')
					otree = self.root
					catdict = {'sport':0,'location':1,'person':2,'organisation':3}
					strs.sort(key=lambda str: catdict[self.checkLookup(str)])
					for str in strs:
						cat = self.checkLookup(str)
						iter = Iterator(otree, str, cat)
						otree = iter.newRoot
					subResult.addSubset(otree)
					result.addSubset(subResult)
				else:
					quer = quer.strip()
					cat = self.checkLookup(quer)
					subResult = SetN('reroot', 'reroot')
					iter = Iterator(self.root, quer, cat)
					subResult.addSubset(iter.newRoot)
					result.addSubset(subResult)
			return result


		def querySimple(self, queryStr):
			queryStr = queryStr.strip()
			cat = self.checkLookup(queryStr)
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
	def checkLookup(self, st):
		return self.querSys.checkLookup(st)
	def query(self, queryStr):
		pass
	def runQuery(self):
		cont = True
		while cont:
			print('Please enter a query with any of the following separated by & and/or |: sportnames, sportpersons, locations, ')
			queryStr = input()
			while queryStr=='':
				print("Empty query. Try again? (Y/N)")
				a = input()
#				os.system('clear')
				if a=='N':
					cont = False
					break
				else:
					queryStr = input()
			
			if queryStr!='':
				self.query = self.querSys.getQueryFn(queryStr)

				finalTree = self.query(self, queryStr)
	#			os.system('clear')
				finalTree.display()
				if len(finalTree.getArticles())==0:
					print("\nYour query did not return any results.")
				print("Run another query? (Y/N)")
				a = input()
	#			os.system('clear')
				if a=='N':
					cont = False
				
				
def trav_test_tree(node,lvl):
	if type(node).__name__=='SetN':
		print(lvl,':SetN:  cat:',node.setCat,'val:',node.setVal)
		for no in node.getChildren():
			trav_test_tree(no,lvl+1)
	else:
		artNodeList[lvl].add(node.artNo)
		print(lvl,': ArtN :',node.artNo)

def test_tree_cat_order(node,li):
	if type(node).__name__=='SetN':
		val = node.setCat
		if val in li:
			a = li.index(val)
			li = li[a:]
			retVal = True
			for no in node.getChildren():
				retVal = retVal&test_tree_cat_order(no,li)
				if not retVal:
					print('Failed at:',no.setVal,no.setCat)
					return retVal
			return retVal
		else:
			return False

	else:
		return True
tree = Tree()
print('Tree Construction Done. Continue?')
#input()
print('Tree testing')
catLi = ['root','sport','location','person','organisation']
root = tree.root
print(test_tree_cat_order(root,catLi))
#tree.root.display()
tree.runQuery()
'''		print('SetN:I:',I,'val:',node.setVal,'cat:',node.setCat)
		input()
		for no in node.getChildren():
			test_tree(no,li,I+1)'''
'''
artNodeList = [set(),set(),set(),set(),set(),set()]
trav_test_tree(tree.root,0)
for s in artNodeList:
	print(sorted(s),'\n')'''
	

def trav_root_list(roots,lvl):
	isSet = type(roots[0]).__name__=='SetN'
	for root in roots:
		if (type(root).__name__=='SetN') != isSet:
			print('Order of sets and/or arts at level',lvl)
			return False
	ans = True
	if isSet:
		v,c = roots[0].setVal,roots[0].setCat
		for root in roots:
			if root.setVal!=v or root.setCat!=c:
				return False
		l = len(roots[0].getChildren())
		for root in roots:
			if len(root.getChildren())!=l:
				return False
		for i in range(l):
			li = []
			for root in roots:
				li.append(root.getChildren()[i])
			ans = ans&trav_root_list(li, lvl+1)
			if not ans:
				return ans
	else:
		a = roots[0].artNo
		for root in roots:
			if root.artNo!=a:
				return False
	return ans
roots = [1,1,1]
roots[0],l = create_initial_tree()
roots[1],l = create_initial_tree()
roots[2],l = create_initial_tree()
print('are multiple trees the same:')
print(trav_root_list(roots,0))
