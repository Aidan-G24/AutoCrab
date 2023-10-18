
from gpiozero import DigitalOutputDevice


class motor:

	def __init__(self, pin, invert):
		
		self.Output = DigitalOutputDevice(pin, active_high=invert)

	def forward



