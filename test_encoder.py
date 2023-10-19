
import pigpio
import time
from motorControl import Decoder
from motorControl import DCMotor


if __name__ == "__main__":


   pos = 0

   encode_pinA, encode_pinB = 7, 8

   def callback(way):

      global pos

      pos += way

      print("pos={}".format(pos))

   pi = pigpio.pi()

   decoder = Decoder(pi, encode_pinA, encode_pinB, callback)

   motor_pin = 23
   pwm_pin = 18
   freq = 10000

   front_left = DCMotor(('front', 'left'), motor_pin, pwm_pin, pi)

   try:
       while True:
           front_left.set_speed(10)
           front_left.set_direction(1)
           time.sleep(300)

   except KeyboardInterrupt:
      front_left.set_speed(0)
      front_left.set_direction(0)      
      decoder.cancel()
      pi.stop()


   