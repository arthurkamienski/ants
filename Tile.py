class Tile():
	def __init__(self, pos, terrain):
		self.terrain = terrain
		self.pos = pos

		self.colonyPher = 0
		self.foodPher = 0
		self.scent = 0
		self.ant = None
		self.colony = False
		self.food = False
		self.obst = False
		self.rect = None
		
		self.color = 'white'

		self.foodPherColors = {
		9:'#CD9504',
		8:'#D2A01F',
		7:'#D8AC3B',
		6:'#DDB857',
		5:'#E3C473',
		4:'#E8CF8F',
		3:'#EEDBAB',
		2:'#F3E7C7',
		1:'#F9F3E3',
		0:'#FFFFFF'
		}

		self.colonyPherColors = {
		9:'#A304BE',
		8:'#AD1FC5',
		7:'#B73BCC',
		6:'#C157D3',
		5:'#CB73DA',
		4:'#D68FE2',
		3:'#E0ABE9',
		2:'#EAC7F0',
		1:'#F4E3F7',
		0:'#FFFFFF'
		}

	def changeColor(self):
		color = 'white'

		if self.ant:
			if self.ant.isSearching():
				color = 'black'
			elif self.ant.isGoing():
				color = 'blue'
				# color = 'black'
			else:
				color = 'brown'
				# color = 'black'
		elif self.isColony():
			color = 'red'
		elif self.isFood():
			color = 'green'
		elif self.isObst():
			color = 'gray'
		else:
			if self.getColonyPher() or self.getFoodPher():
				if self.getColonyPher() > self.getFoodPher():	
					color = self.colonyPherColors[self.colonyPher//100]
					# color = self.colonyPherColors[9]
				else:
					color = self.foodPherColors[self.foodPher//100]
					# color = self.foodPherColors[9]

		if color != self.color:
			self.color = color
			self.terrain.addChangedTile(self)

		self.color = color

	def isFree(self):
		free = False
		if not self.getAnt() and not self.isObst():
			free = True
		return free

	def decreasePher(self, amount):
		self.colonyPher = max(self.colonyPher-amount, 0)
		self.foodPher = max(self.foodPher-amount, 0)
		self.changeColor()

	def getPher(self):
		return self.pher

	def getScent(self):
		return self.scent

	def getFoodPher(self):
		return self.foodPher

	def getColonyPher(self):
		return self.colonyPher

	def getAnt(self):
		return self.ant

	def isColony(self):
		return self.colony

	def isFood(self):
		return self.food

	def isObst(self):
		return self.obst

	def setAnt(self, ant):
		self.ant = ant
		self.changeColor()

	def setScent(self, scent):
		self.scent = scent
		self.changeColor()

	def setFoodPher(self, foodPher):
		self.foodPher = foodPher
		self.changeColor()

	def setColonyPher(self, colonyPher):
		self.colonyPher = colonyPher
		self.changeColor()

	def setColony(self, colony):
		self.colony = colony
		self.changeColor()

	def setFood(self, food):
		self.food = food
		self.changeColor()

	def setObst(self, obst):
		self.obst = obst
		self.changeColor()

	def getColor(self):
		return self.color

	def isChanged(self):
		return self.changed

	def getRect(self):
		return self.rect

	def setRect(self, rect):
		self.rect = rect

	def getPos(self):
		return self.pos