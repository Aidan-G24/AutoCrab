

from motorControl import CarControl
from config import pins
import time


if __name__ == "__main__":

	Crab = CarControl(pins)
	print("init complete")

	try:
		print("Start Move forward")
		Crab.car_move("forward", 50, 500)
		time.sleep(2)
		Crab.car_move("left", 50, 500)
		time.sleep(2)
		Crab.car_move("backward", 50, 500)
		time.sleep(2)
		Crab.car_move("right", 50, 500)
		time.sleep(2)
		# Crab.car_move("clockwise", 75, 10000)
		# time.sleep(6)
		# Crab.car_move("counter", 75, 10000)
		# Crab.car_off()

	except KeyboardInterrupt:
		Crab.car_off()


