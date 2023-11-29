

from motorControl import CarControl
from grid import Grid
from lidarControl import Lidar
from config import pins
import math
import cmath
import time


def calculate_angle(cur_angle, desired_angle):

	diff = desired_angle - cur_angle

	# 0 < diff < 180
	if diff >=0 and diff <= 180:
		direction = "counter"
		angle = diff

	elif diff > 180:
		direction = "clockwise"
		angle = 360 - diff

	elif diff >= -180 and diff < 0:
		direction = "counter"
		angle = abs(diff)

	else:
		direction = "clockwise"
		angle = 360 + diff

	return direction, angle


if __name__ == "__main__":

	crab = CarControl(pins)
	grid = Grid()
	lidar = Lidar()

	speed = 25

	try:
		while True:
			# ask for user input
			x_target = input("Enter Target Location X: ")
			y_target = input("Enter Target Location Y: ")
			x_num, y_num = int(x_target), int(y_target)

			x_num -= grid.x
			y_num -= grid.y

			direct = input("Would you like to travel along the shortest path (y/n)? ")

			if direct == 'y':

				rect = complex(x_num, y_num)
				distance, angle = cmath.polar(rect)
				# distance = math.sqrt(x_num**2 + y_num**2)

				direction, angle = calculate_angle(grid.angle, math.degrees(angle))

				print(f"direction: {direction}, angle: {angle}")

				crab.rotate(direction, speed, angle, lidar)
				grid.update_angle(angle, direction)

				actual_dist = crab.car_move("forward", speed, distance, lidar)
				grid.update_pos(actual_dist, "forward")

			elif direct == 'n':
				if x_num == 0:
					pass
				elif x_num < 0:
					direction = "backward"
				else:
					direction = "forward"

				actual_dist = crab.car_move(direction, speed, abs(x_num), lidar)
				grid.update_pos(actual_dist, direction)

				if y_num == 0:
					pass
				elif y_num < 0:
					direction = "right"
				else:
					direction = "left"
				
				actual_dist = crab.car_move(direction, speed, abs(y_num), lidar)
				grid.update_pos(actual_dist, direction)

				print(f"grid.x: {grid.x}, grid.y: {grid.y}")

			else:
				print("Invalid input, either input y or n.")
				continue


	except KeyboardInterrupt:
		crab.car_off()