
import time
import lgpio
from gpiozero import RotaryEncoder

motor = 23
PWM = 18
freq = 10000

# open the gpio chip and set the motor pin as output
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, motor)

encoder_pins = [20, 21]

encode = RotaryEncoder(encoder_pins[0], encoder_pins[1])


try:
    while True:
        print("Turn On")
        # Turn the GPIO pin on
        lgpio.gpio_write(h, motor, 1)
        lgpio.tx_pwm(h, PWM, freq, 25)
        time.sleep(5)
        print("Turn Off")

        # Turn the GPIO pin off
        lgpio.gpio_write(h, motor, 0)
        lgpio.tx_pwm(h, PWM, freq, 0)
        print("encoder has a value of ", encode.values)	
        time.sleep(3)

        print("Turn Other Direction")
        lgpio.tx_pwm(h, PWM, freq, 100)
        time.sleep(5)

        print("Turn Off")
        # Turn the GPIO pin off
        lgpio.tx_pwm(h, PWM, freq, 0)
        print("encoder has a value of ", encode.values)
        time.sleep(3)

except KeyboardInterrupt:
    lgpio.gpio_write(h, motor, 0)
    lgpio.tx_pwm(h, PWM, freq, 0)
    lgpio.gpiochip_close(h)

