

class Grid:

	def __init__():
		self.x = 0
		self.y = 0
		self.angle = 0
		self.diameter = 715 	# mm

	def update_pos(self, distance, direction):

		if direction == "forward":
			x_inc = math.cos(math.radians(self.car_angle)) * distance
			y_inc = math.sin(math.radians(self.car_angle)) * distance

		elif direction == "backward":
			x_inc = math.cos(math.radians(self.car_angle + 180)) * distance
			y_inc = math.sin(math.radians(self.car_angle + 180)) * distance

		elif direction == "left":
			x_inc = math.cos(math.radians(self.car_angle + 90)) * distance
			y_inc = math.sin(math.radians(self.car_angle + 90)) * distance

		elif direction == "right":
			x_inc = math.cos(math.radians(self.car_angle + 270)) * distance
			y_inc = math.sin(math.radians(self.car_angle + 270)) * distance

		else:
			raise Exception("invalid input direction to Class: Grid; Method: update_pos")

		self.x += x_inc
		self.y += y_inc


	def update_angle(self, angle, direction):

		if direction == "clockwise":
			angle_inc = distance / (self.diameter*math.pi) * -360

		elif direction == "counter":
			angle_inc = distance / (self.diameter*math.pi) * 360

		else:
			raise Exception("invalid input direction to Class: Grid; Method: update_angle")


		self.angle += angle_inc
		self.angle = self.angle % 360
		