
import pigpio
from motorControl import CarControl
from time import sleep

servo_pin = 25

pi = pigpio.pi()

servo = CarControl.Servo(('front', 'left'), servo_pin, pi)

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
	servo.off()
