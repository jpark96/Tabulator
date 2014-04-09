import json
from pprint import pprint
from Race import *

class Candidate:

	def __init__(self, number, name, position, party):
		self.number = number
		self.name = name
		self.position = position
		self.party = party
		self.score = 0
		self.ballots = []
		self.state = RUNNING

	def __eq__(self, other):
		return (other.number == self.number) and (other.name == self.name) and (other.position == self.position) and (other.party == self.party)

	def __str__(self):
		return str(self.number) + ". " + self.name + " " + str(self.position) + " " + self.party + " SCORE: " + str(self.score) + " STATE: " + STATES[self.state]

	def __hash__(self):
		return self.number

class Election:

	def __init__(self, frame):
		# self.ballots is an array of Ballot objects
		self.ballots = []

		# self.candidates is a dictionary mapping positions to an array of Candidate objects
		self.candidates = {}

		# self.frame is the GUI frame that's displaying the election
		self.frame = frame

		self.race = None

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
		with open(filepath) as data_file:
			data = json.load(data_file)
		self.candidates[SENATOR] = []
		for candidate in data["senator"]:
			self.__addJSONCandidate__(candidate, SENATOR)
		self.candidates[PRESIDENT] = []
		for candidate in data["president"]:
			self.__addJSONCandidate__(candidate, PRESIDENT)
		self.candidates[EXECUTIVE_VP] = []
		for candidate in data["executive_vp"]:
			self.__addJSONCandidate__(candidate, EXECUTIVE_VP)
		self.candidates[EXTERNAL_VP] = []
		for candidate in data["external_vp"]:
			self.__addJSONCandidate__(candidate, EXTERNAL_VP)
		self.candidates[ACADEMIC_VP] = []
		for candidate in data["academic_vp"]:
			self.__addJSONCandidate__(candidate, ACADEMIC_VP)
		self.candidates[STUDENT_ADVOCATE] = []
		for candidate in data["student_advocate"]:
			self.__addJSONCandidate__(candidate, STUDENT_ADVOCATE)

	def __addJSONCandidate__(self, candidate, position):
		self.candidates[position].append(Candidate(int(candidate["number"]), candidate["name"], position, candidate["party"]))

	def displayCandidates(self):
		for position in self.candidates:
			print(position)
			print("-------------------------------------------------")
			candidates = self.candidates[position]
			for candidate in candidates:
				print(candidate)
			print("")

	def startRace(self, position):
		candidates = self.candidates[position]
		if not self.ballots: raise ElectionError("No ballots have been entered.")
		self.race = Race(self, position, candidates, self.ballots)
		if (position != SENATOR):
			self.stepFunction = self.race.runStepExecutives
		else:
			self.stepFunction = self.race.runStepSenator

	def iterateRace(self):
		if self.race:
			return self.stepFunction()

	def finishRace(self):
		if self.race:
			status = CONTINUE
			while status != FINISHED:
				status = self.stepFunction()
				if status == STOP:
					self.race.candidates.sort(key=lambda x: -1 * x.score)
					for cand in self.race.candidates:
						print(cand)
					raw_input()
				pass
		


	# def tally(self, position):
	# 	candidates = self.candidates[position]
	# 	if not self.ballots: raise ElectionError("No ballots have been entered.")

	# 	race = Race(self, position, candidates, self.ballots)
	# 	if position != SENATOR:
	# 		return race.applyBallotExecutives()
	# 	else:
	# 		self.iterator = race.applyBallotSenator()

	# def step(self):
	# 	# print("stepped")
	# 	return self.iterator.next()

	








