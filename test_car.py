

from motorControl import CarControl
from config import pins




if __name__ == "__main__":

	Crab = CarControl(pins)


	try:
		Crab.test_module()

	except KeyboardInterrupt:
		Crab.car_off()


