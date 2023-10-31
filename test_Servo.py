
import pigpio
from motorControl import Servo
from time import sleep

servo_pin = 4

pi = pigpio.pi()

servo = Servo(('front', 'left'), servo_pin, pi)

try:
	while True:
		print('angle 0')
		servo.angle(0)
		sleep(5)
		print('angle 90')
		servo.angle(90)
		sleep(5)
		print('angle 180')
		servo.angle(180)
		sleep(5)
except KeyboardInterrupt:
	servo.servo_off()
