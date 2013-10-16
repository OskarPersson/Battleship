class Ship:
	def __init__(self, size):
		self.parts = []
		for x in range(size):
			self.parts.append(True)