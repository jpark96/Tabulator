from constants import *
import math
import time

class Race:
# A race refers to an election for one particular position

	def __init__(self, election, position, candidates, ballots):
		self.election = election
		self.position = position
		self.candidates = candidates
		self.ballots = ballots
		self.validVotes = 0
		self.winners = 0
		self.spentBallots = 0
		self.iterationNumber = 0
		
		self.finished = False
		self.current_ballots = ballots
		self.redistribute_ballots = []
		self.numValidVotes = self.countValidVotes(ballots)
		if position != SENATOR:
			self.quota = round((self.numValidVotes + 1)/2.0)
		else:
			self.quota = round(float(self.numValidVotes)/(NUM_SENATORS+1) + 1)
		self.winner = []

		# For senators
		self.current_winners = []
		self.current_runners = candidates[:]

		# (HACK) Can't hash candidates, so temporarily use their candidate number as a key
		self.numToCandidate = {candidate.number: candidate for candidate in candidates}

	def countValidVotes(self, ballots):
		count = 0
		for ballot in ballots:
			if self.position not in ballot.votes.keys():
				raise ElectionError("Position not found in ballot!")
			vote = ballot.votes[self.position]
			if vote:
				count += 1
		return count

	def runStepExecutives(self):
		if self.finished:
			return FINISHED
		if self.current_ballots:
			ballot = self.current_ballots.pop(0)
			if ballot.candidate and ballot.candidate.state == LOSE:
				ballot.candidate.score -= ballot.value
			self.applyBallot(ballot)
			return CONTINUE
		elif self.numOfRunners() == 1:
			for candidate in self.candidates:
				if candidate.state == RUNNING:
					candidate.state = WIN
					self.finished = True
					self.winner.append(candidate)
					return FINISHED
		for candidate in self.candidates:
			if candidate.score >= self.quota:
				candidate.state = WIN
				self.finished = True
				self.winner.append(candidate)
				return FINISHED
		self.candidates.sort(key=lambda x: -1 * x.score)
		for candidate in reversed(self.candidates):
			if candidate.state == RUNNING:
				self.current_ballots += candidate.ballots
				candidate.state = LOSE
				return STOP

	def runStepSenator(self):
		if self.finished:
			return FINISHED
		if self.current_ballots:
			ballot = self.current_ballots.pop(0)
			if ballot.candidate and ballot.candidate.state == LOSE:
				ballot.candidate.score -= ballot.value
			self.applyBallot(ballot)
			# ballot.candidate.score = self.round(ballot.candidate.score, 4)
			return CONTINUE

		if (len(self.current_winners) + len(self.current_runners)) <= NUM_SENATORS:
			self.current_runners.sort(key=lambda x: -1 * x.score)
			self.winner = self.current_winners + self.current_runners
			self.finished = True
			return FINISHED
		if len(self.current_winners) == NUM_SENATORS:
			self.winner = self.current_winners
			self.finished = True
			return FINISHED

		self.current_runners.sort(key=lambda x: x.score)
		top_candidate = self.current_runners[-1]

		# Someone Quota'd
		if top_candidate.score >= self.quota:
			top_candidate.state = WIN
			self.current_runners.pop()
			self.current_winners.append(top_candidate)
			for ballot in top_candidate.ballots:
				ballot.value = ballot.value * float(top_candidate.score - self.quota)/top_candidate.score
				self.current_ballots.append(ballot)
			top_candidate.score = self.quota
			top_candidate.quotaPlace = NUM_SENATORS - len(self.current_winners) + 1
			return CONTINUE
		else:
			last_candidate = self.current_runners.pop(0)
			self.current_ballots += last_candidate.ballots
			last_candidate.state = LOSE
			return STOP


	def applyBallot(self, ballot):
		"""Increment a candidates score, and pop his number off the vote"""
		if self.position not in ballot.votes.keys():
			raise ElectionError("Position not found in ballot!")
		vote = ballot.votes[self.position]

		while True:
			if not vote:
				self.spentBallots += ballot.value
				return False
			candidate_num = int(vote.pop(0))
			if candidate_num not in self.numToCandidate.keys():
				raise ElectionError("Candidate " + str(candidate_num) + " not found!")
			if self.numToCandidate[candidate_num].state == RUNNING:
				break

		candidate = self.numToCandidate[candidate_num]
		candidate.score += ballot.value
		candidate.ballots.append(ballot)
		ballot.candidate = candidate
		return True


	def numOfRunners(self):
		"""Return the number of candidates still running"""
		count = 0
		for candidate in self.candidates:
			if candidate.state == RUNNING:
				count += 1
		return count

	def initializeFirstVotes(self, ballot):
		if self.applyBallot(ballot):
			self.validVotes += 1


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

		self.candidate = None
		self.votes = votes
		self.value = 1

	def setValue(self, val):
		self.value = val

	def __str__(self):
		return str(self.votes)
	

