class Battlefield:
	def __init__(self):
		self.field = {}
		cellNumber = 10 
		for code in range(ord('A'), ord('K')):
			self.field[chr(code)] = {}
			for j in range(1, cellNumber + 1):
				 k = {j:False}
				 self.field[chr(code)][j] = False