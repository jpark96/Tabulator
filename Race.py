from constants import *
class Race:
# A race refers to an election for one particular position

	def __init__(self, position, candidates, ballots):
		# Candidates is an array of Candidate objects
		# CandidateScore is a dictionary matching a candidate number to number of votes
		self.position = position
		self.candidates = candidates
		self.ballots = ballots
		self.validVotes = 0
		self.winners = 0

		# (HACK) Can't hash candidates, so temporarily use their candidate number as a key
		self.numToCandidate = {candidate.number: candidate for candidate in candidates}

	def applyBallotExecutives(self):
		"""Run the elections for executive races"""
		for ballot in self.ballots:
			self.initializeFirstVotes(ballot)

		quota = (self.validVotes + 1)/2.0

		count = 0
		while self.winners < 1:
			print("---------- count: " + str(count))
			count += 1
			for candidate in self.candidates:
				print(candidate.name + ": " + str(candidate.score));
			if self.numOfRunners() == 1:
				for candidate in self.candidates:
					if candidate.state == RUNNING:
						candidate.state = WIN
						self.winners = 1
						return candidate

			for candidate in self.candidates:
				if candidate.score >= quota:
					candidate.state = WIN
					self.winners = 1
					return candidate

			self.candidates.sort(key=lambda x: x.score)
			for candidate in self.candidates:
				if candidate.state == RUNNING:
					for ballot in candidate.ballots:
						self.applyBallot(ballot)
					candidate.state = LOSE
					break

	def applyBallotSenator(self):
		for ballot in self.ballots:
			self.initializeFirstVotes(ballot)

		quota = self.validVotes/(NUM_SENATORS+1) + 1

		current_winners = []
		current_runners = self.candidates.copy()
		current_ballots = []

		while True:
			if (len(current_winners) + len(current_runners)) <= NUM_SENATORS:
				current_winners += current_runners
				return current_winners

			top_candidate = current_runners.sort(key=lambda x: x.score)[-1]

			if top_candidate.score >= quota:
				top_candidate.state = WIN
				current_runners.pop()
				current_winners.append(top_candidate)
				for ballot in top_candidate.ballots:
					ballot.value = float(ballot.value + (top_candidate.score - quota))/top_candidate.score
					current_ballots.append(ballot)
			else if current_ballots:
				for ballot in current_ballots:
					self.applyBallot(ballot)
			else:
				last_candidate = current_runners.pop(0)
				for ballot in last_candidate.ballots:
					self.applyBallot(ballot)
				last_candidate.state = LOSE
				
			if len(current_winners) == NUM_SENATORS:
				return current_winners



	def applyBallot(self, ballot):
		"""Increment a candidates score, and pop his number off the vote"""
		if self.position not in ballot.votes.keys():
			return
		vote = ballot.votes[self.position]

		while True:
			if not vote:
				return
			candidate_num = vote.pop(0)
			if candidate_num not in self.numToCandidate.keys():
				raise ElectionError("Candidate " + str(candidate_num) + " not found!")
			if self.numToCandidate[candidate_num].state == RUNNING:
				break

		candidate = self.numToCandidate[candidate_num]
		candidate.score += 1
		candidate.ballots.append(ballot)

	def numOfRunners(self):
		"""Return the number of candidates still running"""
		count = 0
		for candidate in self.candidates:
			if candidate.state == RUNNING:
				count += 1
		return count

	def initializeFirstVotes(self, ballot):
		self.applyBallot(ballot)
		self.validVotes += 1





	def applyBallots(self):
		# First pass
		for ballot in self.ballots:
			self.initializeFirstVotes(ballot)
		
		if self.position == SENATOR:
			while(self.winners <= 20):
				self.checkQuota()
				self.redistribute()
		else:
		# See if any executive won through quota'ing
			for candidate in self.candidates:
				if candidate.state == WIN:
					return

	def redistribute(self):
		"""Redistribute the votes of the candidate who is still running and has the least votes."""
		self.candidates.sort(key=lambda x: x.score)
		for candidate in self.candidates:
			if candidate.state == RUNNING:
				for ballot in candidate.ballots:
					self.applyBallot(ballot)
				candidate.state = LOSE
				break

	def checkQuota(self):
		"""Check if any candidates have quota'd and update their status."""
		if self.position != SENATOR:
			quota = self.validVotes/(NUM_SENATORS+1) + 1
		else:
			quota = (self.validVotes + 1)/2.0
		for candidate in self.candidates:
			if candidate.score >= quota:
				candidate.state = WIN
				self.winners += 1


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
		self.value = 1

	def setValue(self, val):
		self.value = val
	

