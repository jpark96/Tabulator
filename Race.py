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
		votes = ballot.votes[self.position]
		for i, candidate_number in enumerate(votes):
			self.candidateVotes[candidate_number] += self.value(i)

	def value(self, rank):
		# The first vote in an array gets a value of 1
		return rank + 1

class Ballot:

	def __init__(self, votes):
		# Votes is a dictionary matching position to an array of candidate numbers.
		# The position of the candidate number in the array refers to rank of the vote.
		self.votes = votes
