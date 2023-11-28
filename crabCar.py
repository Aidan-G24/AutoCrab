

from motorControl import CarControl
from grid import Grid
from config import pins
import math
import time



if __name__ == "__main__":

	crab = CarControl(pins)
	grid = Grid()

	speed = 25

	try:
		while True:
			# ask for user input
			x_target = input("Enter Target Location X: ")
			y_target = input("Enter Target Location Y: ")
			x_num, y_num = int(x_target), int(y_target)

			direct = input("Would you like to travel along the shortest path (y/n)? ")

			if direct == 'y':
				angle = math.tan(x/y)
				distance = math.sqrt(x**2 + y**2)

				printf("TODO")

			elif direct == 'n':
				if x_num < 0:
					direction = "backward"
				else:
					direction = "forward"

				crab.car_move(direction, speed, math.abs(x_num))

				if y_num < 0:
					direction = "right"
				else:
					direction = "left"
				
				crab.car_move(direction, speed, math.abs(x_num))

			else:
				print("Invalid input, either input y or n.")
				continue

			# move car angle back to 0 after movement
			if grid.angle != 0:
				if grid.angle < 180:
					direction = "clockwise"
				else:
					direction = "counter"

				crab.rotate(direction, speed, grid.angle)

	except KeyboardInterrupt:
		Crab.car_off()