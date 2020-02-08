class Node:
	def display(self):
		pass
	def getArticles(self):
		pass
	def addSubset(self, Subset):
		pass

class SetN(Node):
	def __init__(self, ID):
		self.children = []
		self.setID = ID
	def display(self):
		for se in self.children:
			se.display()
	def addSubset(self, Subset):
		self.children.append(Subset)
	def getArticles(self):
		li = []
		for se in self.children:
			li.extend(se.getArticles())
		return li

class ArtN(Node):
	def __init__(self, no):
		self.artNo = no
	def display(self):
		i = 1
		f = open("ArticlesFinal.csv","r")
		line = f.readline()
		while line:
			line = f.readline()
			if i==self.artNo:
				print(line)
				print('--------------------------------------------------------------------------')
				break
			i += 1
	def getArticles(self):
		return list(self)
		
root = SetN('root')
cri = SetN('cricket')
ot = SetN('other')
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
print("CALLING ON A LEAF NODE:")
ot.children[0].display()
