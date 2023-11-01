

from motorControl import CarControl
from config import pins
import time



if __name__ == "__main__":

	Crab = CarControl(pins)
	print("init complete")

	try:
		while True:
			Crab.turn_motors()
			time.sleep(100)


	except KeyboardInterrupt:
		Crab.car_off()


