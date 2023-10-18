
import pigpio
from motorControl import Servo
from time import sleep

servo_pin = 25

pi = pigpio.pi()

servo = Servo(('front', 'left'), 25, pi)

try:
	while True:
		print('angle 0')
		servo.set_angle(0)
		sleep(5)
		print('angle 90')
		servo.set_angle(90)
		sleep(5)
		print('angle 180')
		servo.set_angle(180)
		sleep(5)
except KeyboardInterrupt:
	servo.servo_off()
