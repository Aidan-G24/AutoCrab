
import time
import pigpio
from motorControl import DCMotor


motor_pin = 23
pwm_pin = 18
freq = 10000


pi = pigpio.pi()

front_left = DCMotor(('front', 'left'), motor_pin, pwm_pin, pi)

try:
    while True:
        front_left.set_speed(50)
        front_left.set_direction(1)
        time.sleep(5)

        front_left.set_speed(0)
        front_left.set_direction(0)
        time.sleep(2)

        front_left.set_speed(100)
        time.sleep(5)

        front_left.set_speed(0)
        time.sleep(2)

except KeyboardInterrupt:
    front_left.set_speed(0)
    front_left.set_direction(0)

