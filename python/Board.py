import tkinter as tk
import Terrain

class Board(tk.Frame):
	def __init__(self, parent, terrain, size=32):
		'''size is the size of a square, in pixels'''

		self.mouseAction = 'make'

		self.terrain = terrain
		self.rows, self.columns = terrain.getSize()
		
		self.size = size


		canvas_width = self.columns * size
		canvas_height = self.rows * size

		tk.Frame.__init__(self, parent)
		self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
								width=canvas_width, height=canvas_height, background="white")
		self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

		# this binding will cause a refresh if the user interactively
		# changes the window size
		self.canvas.bind("<Configure>", self.refresh)

		self.create()

	def makeRect(self, tile):
		x1 = (tile.getPos()[0] * self.size)
		y1 = (tile.getPos()[1] * self.size)
		x2 = x1 + self.size
		y2 = y1 + self.size
		rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=tile.getColor())
		self.canvas.tag_bind(rect, '<B1-Motion>', self.onTileClickHover)
		self.canvas.tag_bind(rect, '<Button-1>', self.onTileClick)
		tile.setRect(rect)

	def onTileClick(self, event):
		coords = self.canvas.coords(event.widget.find_closest(event.x, event.y))

		tile = self.terrain.getTile((int(coords[0]/self.size), int(coords[1]/self.size)))
		self.terrain.addChangedTile(tile)
		
		if tile.isFree():
			self.mouseAction = 'make'
			tile.setObst(True)
		else:
			self.mouseAction = 'erase'
			tile.setObst(False)

	def onTileClickHover(self, event):
		coords = self.canvas.coords(event.widget.find_closest(event.x, event.y))

		tile = self.terrain.getTile((int(coords[0]/self.size), int(coords[1]/self.size)))
		self.terrain.addChangedTile(tile)
		
		if tile.isFree():
			if self.mouseAction == 'make':
				tile.setObst(True)
		else:
			if self.mouseAction == 'erase':
				tile.setObst(False)

	def create(self):
		for tile in self.terrain.getTiles():
			self.makeRect(tile)

	def update(self):
		for tile in self.terrain.getChangedTiles():
			self.canvas.itemconfig(tile.getRect(), fill=tile.getColor())

		self.terrain.setChangedTiles([])

	def refresh(self, event):
		xsize = int((event.width-1) / self.columns)
		ysize = int((event.height-1) / self.rows)
		self.size = min(xsize, ysize)

		self.canvas.delete('all')
		self.create()