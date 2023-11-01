

from motorControl import CarControl
from config import pins
import time



if __name__ == "__main__":

	Crab = CarControl(pins)
	print("init complete")

	try:
		while True:
			Crab.test_module(2)


	except KeyboardInterrupt:
		Crab.car_off()


