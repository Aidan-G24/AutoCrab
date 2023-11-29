

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


def roomba_mode(crab, grid, lidar, speed):

	while True:

		actual_pos = crab.car_move("forward", speed, float("infinity"), lidar)
		grid.update_pos(actual_pos, "forward")

		while lidar.check_distance() == 1:
			if grid.angle == 315:
				print("Car is Stuck, shutting down")
				crab.car_off()
				exit(0)
			crab.rotate("clockwise", speed, 45, lidar)
			grid.update_angle(45, "clockwise")



if __name__ == "__main__":

	crab = CarControl(pins)
	grid = Grid()
	lidar = Lidar()

	speed = 25

	try:
		roomba = Input("Would you like to enter Roomba Mode (y/n)? ")
		if roomba == "y":
			roomba_mode(crab, grid, lidar, speed)
		elif roomba == "n":
			pass
		else:
			print("Incorrect input. Shutting down...")

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

				if grid.angle != angle:
					crab.rotate(direction, speed, int(angle), lidar)
					grid.update_angle(int(angle), direction)

				actual_dist = crab.car_move("forward", speed, distance, lidar)
				grid.update_pos(int(actual_dist), "forward")

				print(f"grid.x: {grid.x}, grid.y: {grid.y}")

			elif direct == 'n':
				if x_num == 0:
					pass
				elif x_num < 0:
					direction = "backward"
				else:
					direction = "forward"

				actual_dist = crab.car_move(direction, speed, abs(x_num), lidar)
				grid.update_pos(int(actual_dist), direction)

				if y_num == 0:
					pass
				elif y_num < 0:
					direction = "right"
				else:
					direction = "left"
				
				actual_dist = crab.car_move(direction, speed, abs(y_num), lidar)
				grid.update_pos(int(actual_dist), direction)

				print(f"grid.x: {grid.x}, grid.y: {grid.y}")

			else:
				print("Invalid input, either input y or n.")
				continue


	except KeyboardInterrupt:
		crab.car_off()