

import pyrealsense2.pyrealsense2 as rs


class Lidar:

	def __init__(self):

		# Create a context object. This object owns the handles to all connected realsense devices
		self.pipeline = rs.pipeline()

		# Configure streams
		config = rs.config()
		config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
		
		# Start streaming
		self.pipeline.start(config)


	def check_distance(self):
		# return 0 if all clear return 1 if object detected

		frames = self.pipeline.wait_for_frames()
		depth = frames.get_depth_frame()
		if not depth: return 0
		count = 0

		# Print a simple text-based representation of the image, by breaking it into 10x20 pixel regions and approximating the coverage of pixels within one meter
		for y in range(480):
			for x in range(640):
				dist = depth.get_distance(x, y)
				if 0 < dist and dist < .8:
					count += 1

		if count > (480 * 640)*.10:
			return 1

		return 0


	def check_left_right(self):

		# return "counter" if the left side of the camera is more clear than right, returns "clockwise" otherwise

		frames = self.pipeline.wait_for_frames()
		depth = frames.get_depth_frame()
		if not depth: return 0
		l_count, r_count = 0, 0

		# Print a simple text-based representation of the image, by breaking it into 10x20 pixel regions and approximating the coverage of pixels within one meter
		for y in range(480):
			for x in range(320):
				l_dist = depth.get_distance(x, y)
				r_dist = depth.get_distance(320 + x, y)
				if 0 < l_dist and l_dist < 0.8:
					l_count += 1

				if 0 < r_dist and r_dist < 0.8:
					r_count += 1

		if l_count > r_count:
			return "counter"
		else:
			return "clockwise"


