import json
from pprint import pprint
from Race import *

class Candidate:

	def __init__(self, number, name, position, party):
		self.number = number
		self.name = name
		self.position = position
		self.party = party

	def __eq__(self, other):
		return (other.number == self.number) and (other.name == self.name) and (other.position == self.position) and (other.party == self.party)

	def __str__(self):
		return str(self.number) + ". " + self.name + " " + str(self.position) + " " + self.party

class Election:

	def __init__(self):
		self.ballots = []
		self.candidates = {}

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

	def loadCandidatesFromJSONFile(self, filepath):
		self.ballots = []
		with open(filepath) as data_file:
			data = json.load(data_file)
		self.candidates[SENATOR] = []
		for candidate in data["senator"]:
			self.candidates[SENATOR].append(Candidate(int(candidate["number"]), candidate["name"], SENATOR, candidate["party"]))

		self.candidates[PRESIDENT] = []
		for candidate in data["president"]:
			self.candidates[PRESIDENT].append(Candidate(int(candidate["number"]), candidate["name"], PRESIDENT, candidate["party"]))

		self.candidates[INTERNAL_VP] = []
		for candidate in data["internal_vp"]:
			self.candidates[INTERNAL_VP].append(Candidate(int(candidate["number"]), candidate["name"], INTERNAL_VP, candidate["party"]))

		self.candidates[EXTERNAL_VP] = []
		for candidate in data["external_vp"]:
			self.candidates[EXTERNAL_VP].append(Candidate(int(candidate["number"]), candidate["name"], EXTERNAL_VP, candidate["party"]))

		self.candidates[ACADEMIC_VP] = []
		for candidate in data["academic_vp"]:
			self.candidates[ACADEMIC_VP].append(Candidate(int(candidate["number"]), candidate["name"], ACADEMIC_VP, candidate["party"]))

		self.candidates[STUDENT_ADVOCATE] = []
		for candidate in data["student_advocate"]:
			self.candidates[STUDENT_ADVOCATE].append(Candidate(int(candidate["number"]), candidate["name"], STUDENT_ADVOCATE, candidate["party"]))

	def displayCandidates(self):
		for position in self.candidates:
			print(position)
			print("-------------------------------------------------")
			candidates = self.candidates[position]
			for candidate in candidates:
				print(candidate)
			print("")








