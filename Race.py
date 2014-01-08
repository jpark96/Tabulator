from constants import *
class Race:
# A race refers to an election for one particular position

	def __init__(self, position, candidates):
		# Candidates is an array of Candidate objects
		# CandidateVotes is a dictionary matching a candidate number to number of votes
		self.position = position
		self.candidates = candidates
		self.candidateVotes = {}
		for candidate in candidates:
			self.candidateVotes[candidate.number] = 0

	def applyBallot(self, ballot):
		if self.position not in ballot.votes.keys():
			return
		votes = ballot.votes[self.position]
		for i, candidate_number in enumerate(votes):
			if candidate_number not in self.candidateVotes.keys():
				raise ElectionError("Candidate " + str(candidate_number) + " not found!")
			self.candidateVotes[candidate_number] += self.value(i)

	def displayResults(self):
		for candidate in self.candidates:
			print(str(candidate.number) + ". " + candidate.name + " " + str(self.candidateVotes[candidate.number]))

	def value(self, rank):
		# The first vote in an array gets a value of 1
		return rank + 1

class ElectionError(Exception):

	def __init__(self, message):
		self.message = message

	def __str__(self):
		return repr(self.message)

class BallotError(ElectionError):
	pass

class Ballot:

	def __init__(self, votes):
		# Votes is a dictionary matching position to an array of candidate numbers.
		# The position of the candidate number in the array refers to rank of the vote.
		for position in votes.keys():
			if position not in POSITIONS:
				raise BallotError("Position " + str(position) + " not found!");
		self.votes = votes

