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
		return self.subsets
	def getArticles(self):
		li = []
		for se in self.subsets:
			if type(se).__name__=='SetN':
				li.extend(se.getArticles())
			else:
				li.append(se)
		return li

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
				print('--------------------------------------------------------------------------')
				break
			i += 1
		
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

ot.display()
print("CLASS NAME: ",type(ot).__name__)
print("CALLING ON A LEAF NODE:")
ot.getChildren()[0].display()
print("CLASS NAME: ",type(ot.getChildren()[0]).__name__)
