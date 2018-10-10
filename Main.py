import tkinter as tk
import time
import Board
import Terrain

def main():
	size = (70, 70)
	food = (3,3)
	colony = (size[0]-4, 3)
	initPatrol = 5
	step = 1


	terrain = Terrain.Terrain(size, colony, food)
	root = tk.Tk()
	board = Board.Board(root, terrain)
	board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
	terrain.setNewPatrolCount(initPatrol)

	for i in range(50):
		terrain.makeObstacle((35, 0+i))

	while 1:
		for i in range(1, step + 1):
			time.sleep(0.01)

			if i == step:
				terrain.iterate()

			board.update()
			root.update_idletasks()
			root.update()

main()