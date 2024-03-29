
import pigpio
import time
import math



class CarControl:
	
	def __init__(self, pins):

		self.pi = pigpio.pi()

		self.init_motors(pins["dir_pins"], pins["pwm_pins"])
		self.init_servos(pins["servo_pins"])
		self.init_encoder(pins["enc_pins"])

		self.wheel_orient = "init"			# Options are : "init" "normal" "crab" "fourtyfive"
		self.car_direction = "init" 		# Options are : "init" "forward" "backward" "left" "right" "clockwise" "counter"
		self.orient_wheels("init")


	def init_motors(self, dir_pins, pwm_pins):

		self.front_left_DC = self.DCMotor(("front", "left"), dir_pins[0], pwm_pins[0], self.pi)
		self.front_right_DC = self.DCMotor(("front", "right"), dir_pins[1], pwm_pins[1], self.pi)
		self.back_left_DC = self.DCMotor(("back", "left"), dir_pins[2], pwm_pins[2], self.pi)
		self.back_right_DC = self.DCMotor(("back", "right"), dir_pins[3], pwm_pins[3], self.pi)


	def init_servos(self, servo_pins):

		self.front_left_servo = self.Servo(("front", "left"), servo_pins[0], self.pi)
		self.front_right_servo = self.Servo(("front", "right"), servo_pins[1], self.pi)
		self.back_left_servo = self.Servo(("back", "left"), servo_pins[2], self.pi)
		self.back_right_servo = self.Servo(("back", "right"), servo_pins[3], self.pi)


	def init_encoder(self, enc_pins):

		self.pos = 0
		ticks_360 = 91

		diameter = 97 # mm

		def callback(way):
			self.pos += math.pi * diameter / (ticks_360)

		self.encoder = self.Decoder(enc_pins[0], enc_pins[1], callback, self.pi)


	def orient_wheels(self, orientation):

		def crab():
			# set servo angles for crab walk
			self.front_right_servo.angle(0)
			self.front_left_servo.angle(90)
			self.back_right_servo.angle(90)
			self.back_left_servo.angle(0)
			return


		def normal():
			# set servo angles for forward driving
			self.front_right_servo.angle(90)
			self.front_left_servo.angle(0)
			self.back_right_servo.angle(0)
			self.back_left_servo.angle(90)
			return


		def fourtyfive():
			# set servo angles for 0 degree turn
			self.front_right_servo.angle(45)
			self.front_left_servo.angle(45)
			self.back_right_servo.angle(45)
			self.back_left_servo.angle(45)
			return


		def init():
			# set all servos to 0
			self.front_right_servo.angle(0)
			self.front_left_servo.angle(0)
			self.back_right_servo.angle(0)
			self.back_left_servo.angle(0)
			return


		if orientation == self.wheel_orient:
			print("Wheel orient is correct")
			return
		
		if orientation == "normal":
			normal()
		elif orientation == "crab":
			crab()
		elif orientation == "fourtyfive":
			crab()
		elif orientation == "init":
			init()
		else:
			print("Input orientation not recognized")
			return 

		self.wheel_orient = orientation

		print("Wheel orient is correct")
		return 


	def test_module(self, time_step):

		print("Begin Testing.")

		def servo_test(servo):

			print(f"now testing: {servo.location[0]} {servo.location[1]} servo.\nWith pin: {servo.pin}")
			time.sleep(time_step)
			print("90 degrees")
			servo.angle(90)
			time.sleep(time_step)
			print("45 degrees")
			servo.angle(45)
			time.sleep(time_step)
			print("0 degrees")
			servo.angle(0)
			time.sleep(time_step)


		def motor_test(motor):

			print(f"now testing: {motor.pos0} {motor.pos1} motor.\n With PWM pin: {motor.pwm_pin} and Dir pin: {motor.dir_pin}")
			time.sleep(1)
			print("motor forward 1/2 speed")
			motor.forward()
			motor.speed(50)
			time.sleep(time_step)
			print("motor off")
			motor.speed(0)
			motor.backward()
			time.sleep(time_step)
			print("motor reverse full speed")
			motor.speed(100)
			time.sleep(time_step)
			motor.off()


		servo_test(self.front_left_servo)
		motor_test(self.front_left_DC)
		servo_test(self.front_right_servo)
		motor_test(self.front_right_DC)
		servo_test(self.back_left_servo)
		motor_test(self.back_left_DC)
		servo_test(self.back_right_servo)
		motor_test(self.back_right_DC)


	def car_move(self, direction, speed, distance, lidar):

		# set all of the wheels to the correct orientation
		if direction == "forward" or direction == "backward":
			self.orient_wheels("normal")

		elif direction == "left" or direction == "right":
			self.orient_wheels("crab")

		elif direction == "clockwise" or direction == "counter":
			self.orient_wheels("fourtyfive")

		else:
			raise Exception("invalid input direction to Class: CarControl; Function: car_move")

		# set all the motors to turn in the correct direction
		set_direction = getattr(self.front_left_DC, direction)
		set_direction()
		set_direction = getattr(self.front_right_DC, direction)
		set_direction()
		set_direction = getattr(self.back_left_DC, direction)
		set_direction()
		set_direction = getattr(self.back_right_DC, direction)
		set_direction()

		time.sleep(1)

		self.pos = 0

		self.front_left_DC.speed(speed)
		self.front_right_DC.speed(speed)
		self.back_left_DC.speed(speed)
		self.back_right_DC.speed(speed)

		while self.pos < distance:
			if direction != "forward":
				continue
			if lidar.check_distance() == 1:
				print("Obstacle detected in path... stopping motors")
				break
			

		self.front_left_DC.speed(0)
		self.front_right_DC.speed(0)
		self.back_left_DC.speed(0)
		self.back_right_DC.speed(0)

		if direction != "clockwise" and direction != "counter":
			print("Successfully reached destination... waiting for next instruction")
		return self.pos


	def rotate(self, direction, speed, angle, lidar):

		# length of car is 715 mm
		circum = 715 * math.pi

		distance = angle/360 * circum

		print(f"distance: {distance}")

		self.car_move(direction, speed, distance, lidar)

		return



	def car_off(self):

		# turn off all pins

		time.sleep(1)
		
		self.back_right_servo.off()
		self.back_left_servo.off()
		self.front_right_servo.off()
		self.front_left_servo.off()

		self.front_left_DC.off()
		self.front_right_DC.off()
		self.back_left_DC.off()
		self.back_right_DC.off()

		self.encoder.cancel()

		self.pi.stop()


	def turn_motors(self):

		self.front_left_DC.forward()
		self.front_right_DC.forward()
		self.back_left_DC.forward()
		self.back_right_DC.forward()

		time.sleep(60)

		
	class DCMotor:

		def __init__(self, location, dir_pin, pwm_pin, pi):
			
			self.pos0 = location[0]		# front or back
			self.pos1 = location[1]		# left or right
			self.dir_pin = dir_pin
			self.pwm_pin = pwm_pin
			self.pi = pi

			
		def speed(self, percent):
			if percent < 0 or percent > 100:
				raise Exception("Input speed is outside of the range [0, 100]")
			self.pi.set_PWM_dutycycle(self.pwm_pin, percent/100 * 255)


		def forward(self):
			if self.pos1 == "right":
				self.pi.write(self.dir_pin, 0)
			else:
				self.pi.write(self.dir_pin, 1)


		def backward(self):
			if self.pos1 == "right":
				self.pi.write(self.dir_pin, 1)
			else:
				self.pi.write(self.dir_pin, 0)


		def left(self):
			if self.pos0 == "front":
				self.pi.write(self.dir_pin, 0)
			else:
				self.pi.write(self.dir_pin, 1)


		def right(self):
			if self.pos0 == "front":
				self.pi.write(self.dir_pin, 1)
			else:
				self.pi.write(self.dir_pin, 0)


		def clockwise(self):
			self.pi.write(self.dir_pin, 0)


		def counter(self):
			self.pi.write(self.dir_pin, 1)


		def off(self):
			self.pi.set_PWM_dutycycle(self.pwm_pin, 0)
			self.pi.write(self.dir_pin, 0)



	class Servo:

		def __init__(self, location, pin, pi):
			self.location = location
			self.pin = pin
			self.pi = pi


		def angle(self, angle):
			if angle < 0 or angle > 265:
				raise Exception("Input servo angle incorrect. Input range: [0, 265]")

			self.pi.set_servo_pulsewidth(self.pin, (2000/270 * angle) + 500)


		def off(self):
			self.pi.set_servo_pulsewidth(self.pin, 0)


	# Class taken from: https://github.com/joan2937/pigpio/blob/master/EXAMPLES/Python/ROTARY_ENCODER/rotary_encoder.py
	class Decoder:

		"""Class to decode mechanical rotary encoder pulses."""

		def __init__(self, gpioA, gpioB, callback, pi):
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
				self.levB = level
				
			if gpio != self.lastGpio: # debounce
				self.lastGpio = gpio

				if gpio == self.gpioA and level == 1:
					if self.levB == 1:
						self.callback(1)
				elif gpio == self.gpioB and level == 1:
					if self.levA == 1:
						self.callback(-1)


		def cancel(self):

			self.cbA.cancel()
			self.cbB.cancel()



