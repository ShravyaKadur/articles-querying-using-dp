class Iterator:

	root = SetN('root', 'root')
	
	def __init__(self, val, root):
		self.root = root
		find(val)
	
	def __iter__(self):
		return self
	
	def next(self):
		pass
	
	def sportFind(self, val):
		spRoot = SetN('sproot', 'sproot')
		spCat = SetN(val, 'sport')
		temp = self.root
		
		for se in temp.subsets:
			if type(se).__name__=='SetN':
				if se.cat=='sport' and se.val==val:
					spCat.addSubset(se.subsets)
		
		spRoot.addSubset(spCat)
		return spRoot

	def locFind(self, val):
		locRoot = SetN('locroot', 'locroot')
		locCat = SetN(val, 'sport')
		temp = self.root
		
		while(temp.subsets != []):
			for se in temp.subsets:
				if type(se).__name__=='SetN':
					if se.cat=='location':
						if se.val==val:
							locCat.addSubset(se.subsets)
					else:
						temp = se
			
		locRoot.addSubset(locCat)
		return locRoot
	
	def personFind(self, val):
		personRoot = SetN('proot', 'proot')
		personCat = SetN(val, 'sport')
		temp = self.root
		
		while(temp.subsets != []):
			for se in temp.subsets:
				if type(se).__name__=='SetN':
					if se.cat=='person':
						if se.val==val:
							personCat.addSubset(se.subsets)
					else:
						temp = se
			
		personRoot.addSubset(personCat)
		return personRoot
	
	def orgFind(self, val):
		orgRoot = SetN('orgroot', 'orgroot')
		orgCat = SetN(val, 'sport')
		temp = self.root
		
		while(temp.subsets != []):
			for se in temp.subsets:
				if type(se).__name__=='SetN':
					if se.cat=='organisation':
						if se.val==val:
							orgCat.addSubset(se.subsets)
					else:
						temp = se
			
		orgRoot.addSubset(orgCat)
		return orgRoot
