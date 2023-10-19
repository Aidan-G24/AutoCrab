
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
		self.pi.hardware_PWM(self.pwm_pin, self.freq, percent * 10000)
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

		self.pi.set_servo_pulsewidth(self.pin, (2000/270 * angle) + 500)

		return 0

	def servo_off(self):
		self.pi.set_servo_pulsewidth(self.pin, 0)


class Decoder:

   """Class to decode mechanical rotary encoder pulses."""

   def __init__(self, pi, gpioA, gpioB, callback):


      self.pi = pi
      self.gpioA = gpioA
      self.gpioB = gpioB
      self.callback = callback

      self.levA = 0
      self.levB = 0

      self.lastGpio = None

      self.pi.set_mode(gpioA, pigpio.INPUT)
      self.pi.set_mode(gpioB, pigpio.INPUT)

      self.pi.set_pull_up_down(gpioA, pigpio.PUD_UP)
      self.pi.set_pull_up_down(gpioB, pigpio.PUD_UP)

      self.cbA = self.pi.callback(gpioA, pigpio.EITHER_EDGE, self._pulse)
      self.cbB = self.pi.callback(gpioB, pigpio.EITHER_EDGE, self._pulse)

   def _pulse(self, gpio, level, tick):

      """
      Decode the rotary encoder pulse.

                   +---------+         +---------+      0
                   |         |         |         |
         A         |         |         |         |
                   |         |         |         |
         +---------+         +---------+         +----- 1

             +---------+         +---------+            0
             |         |         |         |
         B   |         |         |         |
             |         |         |         |
         ----+         +---------+         +---------+  1
      """

      if gpio == self.gpioA:
         self.levA = level
      else:
         self.levB = level;

      if gpio != self.lastGpio: # debounce
         self.lastGpio = gpio

         if   gpio == self.gpioA and level == 1:
            if self.levB == 1:
               self.callback(1)
         elif gpio == self.gpioB and level == 1:
            if self.levA == 1:
               self.callback(-1)

   def cancel(self):

      """
      Cancel the rotary encoder decoder.
      """

      self.cbA.cancel()
      self.cbB.cancel()



