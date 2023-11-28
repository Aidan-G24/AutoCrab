

from motorControl import CarControl
from config import pins
import time


if __name__ == "__main__":

	Crab = CarControl(pins)
	print("init complete")
	speed = 25
	distance = 500

	try:
		time.sleep(2)
		print("Start Move forward")
		Crab.car_move("forward", speed, distance)
		time.sleep(2)
		Crab.car_move("left", speed, distance)
		time.sleep(2)
		Crab.car_move("backward", speed, distance)
		time.sleep(2)
		Crab.car_move("right", speed, distance)
		time.sleep(2)
		Crab.car_rotate("clockwise", speed, 90)
		time.sleep(2)
		Crab.car_rotate("counter", speed, 90)
		time.sleepd(2)
		Crab.car_off()

	except KeyboardInterrupt:
		Crab.car_off()

