

from motorControl import CarControl
from config import pins
import time


if __name__ == "__main__":

	Crab = CarControl(pins)
	print("init complete")

	try:
		Crab.car_move("forward", 75, 1000)
		time.sleep(60)

	except KeyboardInterrupt:
		Crab.car_off()


