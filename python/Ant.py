import random

class Ant():
	def __init__(self, pos, number):
		self.scentDecreaseRate = 0.8

		self.number = number

		self.pos = pos
		self.lastPos = None
		
		self.searching = False
		self.going = True
		self.comingBack = False

		self.foodPher = 0
		self.colonyPher = 999

	def update(self, terrain):
		self.decreasePher()
		self.changeStatus(terrain)
		self.move(terrain)

	def decideSearching(self):
		self.searching = random.randrange(100) == 0

	def changeStatus(self, terrain):
		currTile = terrain.getTile(self.pos)

		if currTile.isFood():
			if self.going:
				self.decideSearching()

			self.going = False
			self.comingBack = True

			self.foodPher = 999
			self.colonyPher = 0
		elif currTile.isColony():
			if  self.comingBack:
				if not random.randrange(5):
					terrain.increaseNewAntCount(1)
				self.decideSearching()

			self.going = True
			self.comingBack = False

			self.foodPher = 0
			self.colonyPher = 999

	def getPossMoves(self, terrain):
		x, y = self.pos
		rows, columns = terrain.getSize()
		moves = []

		minx = max(0, x-1)
		maxx = min(rows, x+2)
		miny = max(0, y-1)
		maxy = min(columns, y+2)

		for i in range(minx, maxx):
			for j in range(miny, maxy):
				if terrain.getTile((i, j)).isFree():
					if (i, j) != self.lastPos:
						moves.append((i, j))
		return moves

	def minDist(self, moves, pos):
		x, y = pos
		minDist = 9999999.0
		move = self.pos

		for m in moves:
			x2, y2 = m
			dist = ((x-x2)**2+(y-y2)**2)**(0.5)

			if minDist > dist and m != self.lastPos:
				minDist = dist
				move = m

		return move

	def chooseMinScentPath(self, moves, terrain):
		minPher = 999999
		newMoves = []

		for move in moves:
			if self.going:
				pher = terrain.getTile(move).getColonyPher()
			else:
				pher = terrain.getTile(move).getFoodPher()
			
			if pher < minPher:
				minPher = pher
				newMoves = [move]
			elif pher == minPher:
				newMoves.append(move)

		return newMoves

	def chooseScentPath(self, moves, terrain):
		mostPher = 0
		newMoves = []

		for move in moves:
			if self.going:
				pher = terrain.getTile(move).getFoodPher()
			else:
				pher = terrain.getTile(move).getColonyPher()
			
			if pher > mostPher:
				mostPher = pher
				newMoves = [move]
			elif pher == mostPher:
				newMoves.append(move)

		return newMoves

	def chooseMove(self, moves, terrain):
		try:	
			if self.searching:
				if random.randrange(2) == 0:
					if self.going:
						move = self.minDist(self.chooseMinScentPath(moves, terrain), terrain.getFood())
					elif self.comingBack:
						move = self.minDist(self.chooseMinScentPath(moves, terrain), terrain.getColony())
				else:
					move = random.choice(moves)
			else:
				if random.randrange(20):
					move = random.choice(self.chooseScentPath(moves, terrain))
				else:
					move = random.choice(moves)
		except IndexError:
			move = self.pos

		return move

	def move(self, terrain):

		move = self.chooseMove(self.getPossMoves(terrain), terrain)
		
		currTile = terrain.getTile(self.pos)

		if move != self.pos:
			self.lastPos = self.pos
		self.pos = move

		nextTile = terrain.getTile(move)

		# if self.foodPher or self.colonyPher:
		self.leavePher(currTile)
		terrain.addPherTile(currTile)
		
		terrain.addChangedTile(currTile)
		terrain.addChangedTile(nextTile)

		currTile.setAnt(None)
		nextTile.setAnt(self)

	def leavePher(self, tile):
		tile.setFoodPher(max(self.foodPher, tile.getFoodPher()))
		tile.setColonyPher(max(self.colonyPher, tile.getColonyPher()))

	def decreasePher(self):
		self.foodPher   = max(self.foodPher   - self.scentDecreaseRate, 0)
		self.colonyPher = max(self.colonyPher - self.scentDecreaseRate, 0)

	def setSearching(self, searching):
		self.searching = searching

	def isSearching(self):
		return self.searching

	def isGoing(self):
		return self.going