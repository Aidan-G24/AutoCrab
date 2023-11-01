

from motorControl import CarControl
from config import pins
import time


if __name__ == "__main__":

	Crab = CarControl(pins)
	print("init complete")

	try:
		print("Start Move forward")
		Crab.turn_motors()
		Crab.car_off()

	except KeyboardInterrupt:
		Crab.car_off()


