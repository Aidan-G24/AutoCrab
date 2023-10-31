

from motorControl import CarControl
from config import pins
import time



if __name__ == "__main__":

	Crab = CarControl(pins)
	print("init complete")

	try:
		time.sleep(60)
		# Crab.test_module()

	except KeyboardInterrupt:
		Crab.car_off()


