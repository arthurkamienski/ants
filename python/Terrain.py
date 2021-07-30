import Tile
import Ant

class Terrain():
	def __init__(self, size, colony, food):
		self.scentDecreaseRate = 0.1

		self.limit = 20

		self.antNumber = 0

		self.ants = []
		self.newAntCount = 0
		self.newPatrolCount = 0

		self.changedTiles = []
		self.pherTiles = []

		self.size = size
		self.grid = [[Tile.Tile((i, j), self) for j in range(size[0])] for i in range(size[1])]

		self.tiles = [tile for row in self.grid for tile in row]

		self.setColony(colony)
		self.setFood(food)

	def iterate(self):
		self.decreaseTilePher()
		self.updateAnts()

		if self.antNumber < self.limit:
			if self.newPatrolCount > 0:
				self.addPatrolAnt()
			elif self.newAntCount > 0:
				self.addAnt()

	def updateAnts(self):
		for ant in self.ants:
			ant.update(self)

	def decreaseTilePher(self):
		newPherTiles = []

		for tile in self.pherTiles:
			tile.decreasePher(self.scentDecreaseRate)
			if tile.getColonyPher() or tile.getFoodPher():
				newPherTiles.append(tile)

		self.pherTiles = newPherTiles

	def addAnt(self):
		colony = self.getTile(self.colony)

		newAnt = None

		if not colony.getAnt():
			newAnt = Ant.Ant(self.colony, self.antNumber)
			self.antNumber = self.antNumber + 1
			self.newAntCount = self.newAntCount - 1
			self.ants.append(newAnt)
			colony.setAnt(newAnt)

		return newAnt

	def addPatrolAnt(self):
		newAnt = self.addAnt()

		if newAnt:
			self.newPatrolCount = self.newPatrolCount - 1
			newAnt.setSearching(True)

	def increaseNewAntCount(self, value=1):
		self.newAntCount = self.newAntCount + value

	def setColony(self, colony):
		tile = self.getTile(colony)
		tile.setColony(True)
		self.colony = colony

	def setFood(self, food):
		tile = self.getTile(food)
		tile.setFood(True)
		# self.distributeFoodScent(food)
		self.food = food

	def makeObstacle(self, coord):
		tile = self.getTile(coord)
		tile.setObst(True)

	def distributeFoodScent(self, pos, radius=4):
		x, y = pos
		rows, columns = self.size

		minx = max(0, x-radius)
		maxx = min(rows, x+radius+1)

		miny = max(0, y-radius)
		maxy = min(columns, y+radius+1)

		for i in range(minx, maxx):
			for j in range(miny, maxy):
				dist = ((x-i)**2+(y-j)**2)**(0.5)
				if dist <= radius:
					self.grid[i][j].setScent(((x-i)**2+(y-j)**2)**(0.5))

	def addPherTile(self, tile):
		if tile not in self.pherTiles:
			self.pherTiles.append(tile)

	def addChangedTile(self, tile):
		self.changedTiles.append(tile)

	def getTile(self, coord):
		return self.grid[coord[0]][coord[1]]

	def getNewAntCount(self):
		return self.newAntCount

	def getColony(self):
		return self.colony

	def getAnts(self):
		return self.ants

	def getSize(self):
		return self.size

	def getGrid(self):
		return self.grid

	def getFood(self):
		return self.food

	def getNewPatrolCount(self):
		return self.newPatrolCount

	def getTiles(self):
		return self.tiles

	def getChangedTiles(self):
		return self.changedTiles

	def getStep(self):
		return self.step

	def setNewPatrolCount(self, newPatrolCount):
		self.newPatrolCount = newPatrolCount

	def setChangedTiles(self, changedTiles):
		self.changedTiles = changedTiles

	def setAnts(self, ants):
		self.ants = ants