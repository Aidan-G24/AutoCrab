

from motorControl import CarControl
from lidarControl import Lidar
from config import pins
import time


if __name__ == "__main__":

	lidar = Lidar()
	Crab = CarControl(pins)
	print("init complete")
	speed = 25
	distance = 500

	try:
		time.sleep(2)
		print("Start Move forward")
		Crab.car_move("forward", speed, distance, lidar)
		time.sleep(2)
		Crab.car_move("left", speed, distance, lidar)
		time.sleep(2)
		Crab.car_move("backward", speed, distance, lidar)
		time.sleep(2)
		Crab.car_move("right", speed, distance, lidar)
		time.sleep(2)
		Crab.rotate("clockwise", speed, 180, lidar)
		time.sleep(2)
		Crab.rotate("counter", speed, 180, lidar)
		time.sleepd(2)
		Crab.car_off()

	except KeyboardInterrupt:
		Crab.car_off()

