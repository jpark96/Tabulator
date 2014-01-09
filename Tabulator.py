import json
from pprint import pprint
from Race import *

class Candidate:

	def __init__(self, number, name, position):
		self.number = number
		self.name = name
		self.position = position

	def __eq__(self, other):
		return (other.number == self.number) and (other.name == self.name) and (other.position == self.position)

class Election:

	def __init__(self):
		self.ballots = []

	def loadBallotsFromJSONFile(self, filepath):
		self.ballots = []
		with open(filepath) as data_file:
			data = json.load(data_file)	
		for json_ballot in data["ballots"]:
			# Create a new dictionary that has keys as integers instead of strings
			votes = {}
			for key in json_ballot.keys():
				try:
					votes[int(key)] = json_ballot[key]
				except ValueError:
					print('Invalid key in json: ' + key)

			ballot = Ballot(votes)
			self.ballots.append(ballot)
