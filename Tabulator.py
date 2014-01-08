class Candidate:

	def __init__(self, number, name, position):
		self.number = number
		self.name = name
		self.position = position

	def __eq__(self, other):
		return (other.number == self.number) and (other.name == self.name) and (other.position == self.position)