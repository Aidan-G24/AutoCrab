
import pigpio
import time
from motorControl import Decoder
from motorControl import DCMotor


if __name__ == "__main__":


   pos = 0

   encode_pinA, encode_pinB = 7, 8

   def callback(way):

      global pos

      ticks_360 = 720

      pos += 360/ticks_360

      #print("pos={}".format(pos))

   pi = pigpio.pi()

   decoder = Decoder(pi, encode_pinA, encode_pinB, callback)

   motor_pin = 23
   pwm_pin = 18
   freq = 10000

   front_left = DCMotor(('front', 'left'), motor_pin, pwm_pin, pi)

   try:
      front_left.speed(50)
      front_left.clockwise()
      while pos < 720:
         continue
      front_left.set_speed(0)


   except KeyboardInterrupt:
      front_left.speed(0)
      front_left.clockwise()  
      decoder.cancel()
      pi.stop()
      print(f"pos={pos}")

   front_left.off()
   front_left.clockwise()
   decoder.cancel()
   pi.stop()
   print(f"pos={pos}")

   