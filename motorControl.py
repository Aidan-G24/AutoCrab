
import pigpio

class DCMotor:

	def __init__(self, location, dir_pin, pwm_pin, pi):
		
		self.pos0 = location[0]		# front or back
		self.pos1 = location[1]		# left or right
		self.dir_pin = dir_pin
		self.pwm_pin = pwm_pin
		self.pi = pi
		self.freq = 10000

		
	def set_speed(self, percent):
		if percent < 0 or percent > 100:
			return -1
		self.pi.hardware_pwm(self.pwm_pin, self.freq, percent * 10000)
		return 0


	def set_direction(self, dir):
		self.pi.write(self.dir_pin, dir)



class Servo:

	def __init__(self, location, pin, pi):
		self.location = location
		self.pin = pin
		self.pi = pi


	def set_angle(self, angle):
		if angle < 0 or angle > 265:
			return -1

		self.pi.set_servo_pulsewidth(self.pin, (2000//270 * angle) + 500)

		return 0

	def servo_off(self):
		self.pi.set_servo_pulsewidth(self.pin, 0)

