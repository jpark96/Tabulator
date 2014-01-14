from constants import *
class Race:
# A race refers to an election for one particular position

	def __init__(self, position, candidates):
		# Candidates is an array of Candidate objects
		# CandidateVotes is a dictionary matching a candidate number to number of votes
		self.position = position
		self.candidates = candidates
		self.candidateVotes = {}

		# (HACK) Can't hash candidates, so temporarily use their candidate number as a key
		self.candidateNumberToCandidate = {}
		self.value = self.absolute_value
		for candidate in candidates:
			self.candidateVotes[candidate.number] = 0
			self.candidateNumberToCandidate[candidate.number] = candidate

	def applyBallot(self, ballot):
		if self.position not in ballot.votes.keys():
			return
		votes = ballot.votes[self.position]
		for i, candidate_number in enumerate(votes):
			if candidate_number not in self.candidateVotes.keys():
				raise ElectionError("Candidate " + str(candidate_number) + " not found!")
			self.candidateVotes[candidate_number] += self.value(i)

	def results(self):
		# Sorts the candidates based on their votes
		number_and_votes = [(number, votes) for number, votes in self.candidateVotes.items()]
		number_and_votes.sort(key=lambda x: -1*x[1])
		
		candidates_list = []
		score_list = []
		for number, votes in number_and_votes:
			candidates_list.append(self.candidateNumberToCandidate[number])
			score_list.append(votes)

		return candidates_list, score_list

	def displayResults(self):
		for candidate in self.candidates:
			print(str(candidate.number) + ". " + candidate.name + " " + str(self.candidateVotes[candidate.number]))

	def absolute_value(self,rank):
		# The first vote in an array gets a value of 1
		return 1

	def inverse_value(self, rank):
		# Value of vote is inverse to its rank
		return 1/(1+rank)

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
		
		# Check that all keys are valid
		for position in votes.keys():
			if position not in POSITIONS:
				raise BallotError("Position " + str(position) + " not found!");

		# Create keys if they no votes were assigned to that position
		for position in POSITIONS:
			if position not in votes.keys():
				votes[position] = []

		self.votes = votes

	

