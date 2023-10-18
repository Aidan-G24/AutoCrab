
import pigpio
from motorControl import Servo
from time import sleep

servo_pin = 25

pi = pigpio.pi()

servo = Servo(('front', 'left'), 25, pi)

try:
	while True:
		servo.set_angle(0)
		sleep(2)
		servo.mid(90)
		sleep(2)
		servo.max(180)
		sleep(2)
except KeyboardInterrupt:
	servo.servo_off()
