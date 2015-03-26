#############################################################
#							Race.py 						#
#			  Created by: Alton Zheng & Yun Park			#
#			   Copyright Elections Council 2013				#
#############################################################

from constants import *
from random import shuffle
# from Tabulator import Candidate 		# Needed for doctest in Race.__init__()
import math
import time
import sys

class Race:
# A race refers to an election for one particular position

	def __init__(self, election, position, candidates, ballots):
		"""Instantiate a Race object.
			@parameters: election (Election), position (int in POSITIONS), candidates (Candidate[]), ballots(Ballot[])
			@return: None

			>>> ballot1 = Ballot({1: [101]})
			>>> ballot2 = Ballot({1: [101]})
			>>> tyrion = Candidate(101, "Tyrion", 1, "Lanister")
			>>> ned = Candidate(102, "Ned", 1, "Stark")
			>>> race = Race(None, 1, [tyrion, ned], [ballot1, ballot2])
			>>> race.election
			>>> race.position
			1
			>>> race.ballots[0].votes
			{1: [101], 2: [], 3: [], 4: [], 5: [], 6: []}
			>>> race.ballots[1].votes
			{1: [101], 2: [], 3: [], 4: [], 5: [], 6: []}
			>>> race.quota
			1.0
		"""
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



	def countValidVotes(self, ballots):		# Used to determine total number of votes cast for the position
		"""Takes in an array of ballots.
			@parameter: ballots (Ballot[])
			@return: count (number of valid votes)

			>>> ballot1 = Ballot({1: [101]})
			>>> ballot2 = Ballot({1: [101]})
			>>> tyrion = Candidate(101, 'Tyrion', 1, 'Lanister')
			>>> ned = Candidate(102, 'Ned', 1, 'Stark')
			>>> race = Race(None, 1, [tyrion, ned], [ballot1, ballot2])
			>>> ballot1 = Ballot({1: [101]})
			>>> ballot2 = Ballot({1: [101]})
			>>> ballot3 = Ballot({1: [101], 3: [102]})
			>>> race.countValidVotes([])
			0
			>>> ballot_array1 = [ballot1, ballot2]
			>>> race.countValidVotes(ballot_array1)
			2
			>>> ballot_array1 = ballot_array1 + [ballot3]
			>>> race.countValidVotes(ballot_array1)
			3
		"""
		count = 0
		for ballot in ballots:
			if self.position not in ballot.votes.keys():
				raise ElectionError("Position not found in ballot!")
			vote = ballot.votes[self.position]
			if vote:
				count += 1
		return count

	def numOfRunners(self):
		"""Return the number of candidates still running in the race.
			@parameter: None
			@return: number_of_runners (int)

			>>> ballot1 = Ballot({2: [101]})
			>>> ballot2 = Ballot({2: [101]})
			>>> tyrion = Candidate(101, 'Tyrion', 2, 'Lanister')
			>>> ned = Candidate(102, 'Ned', 2, 'Stark')
			>>> race = Race(None, 2, [tyrion, ned], [ballot1, ballot2])
			>>> race.numOfRunners()
			2
			>>> race.runStepExecutives() 		# Apply first ballot
			1
			>>> race.runStepExecutives() 		# Apply second ballot
			1
			>>> race.runStepExecutives() 		# Make tyrion win
			2
			>>> race.numOfRunners() 			
			1
		"""
		count = 0
		for candidate in self.candidates:
			if candidate.state == RUNNING:
				count += 1
		return count

		def numOfWinners(self):
			"""Return the number of candidates who won the race.
				@parameter: None
				@return: number_of_runners (int)

				>>> ballot1 = Ballot({2: [101]})
				>>> ballot2 = Ballot({2: [101]})
				>>> tyrion = Candidate(101, 'Tyrion', 2, 'Lanister')
				>>> ned = Candidate(102, 'Ned', 2, 'Stark')
				>>> race = Race(None, 2, [tyrion, ned], [ballot1, ballot2])
				>>> race.numOfWinners()
				0
				>>> race.runStepExecutives() 		# Apply first ballot
				1
				>>> race.runStepExecutives() 		# Apply second ballot
				1
				>>> race.runStepExecutives() 		# Make tyrion win
				2
				>>> race.numOfWinners() 			
				1
			"""
		count = 0
		for candidate in self.candidates:
			if candidate.state == WIN:
				count += 1
		return count

	def runStepExecutives(self):
		"""Runs one iteration of the executive race. This method does one of the following actions:
				1. If there are ballots in the race, apply the first ballot in the array.
				2. If there is only one runner, make that runner win.
				3. If candidate has reached quota, make the candidate win by setting the candidate's score to quota, setting candidate's state
					to win, and return FINISHED (2).
				4. Else, eliminate the lowest candidate and redistribute his vote.
			@parameter: None
			@return: STOP, CONTINUE, FINISHED (0, 1, 2)

			>>> ballot1 = Ballot({2: [101]})
			>>> ballot2 = Ballot({2: [101]})
			>>> tyrion = Candidate(101, 'Tyrion', 2, 'Lanister')
			>>> ned = Candidate(102, 'Ned', 2, 'Stark')
			>>> race = Race(None, 2, [tyrion, ned], [ballot1, ballot2])
			>>> len(race.current_ballots)
			2
			>>> race.runStepExecutives() 		# Applies ballot1
			1
			>>> len(race.current_ballots)
			1
			>>> race.runStepExecutives() 		# Applies ballot2
			1
			>>> len(race.current_ballots)
			0
			>>> race.numOfRunners()
			2
			>>> race.runStepExecutives() 		# tyrion's score is equal to quota, so make him win.
			2
		"""
		# CONTINUE to apply current_ballots while it exists.
		if self.current_ballots:
			self.applyCurrentBallot()
			return CONTINUE
		# FINISHED if there is only one runner.
		elif self.numOfRunners() == 1:
			for candidate in self.candidates:
				if candidate.state == RUNNING:
					candidate.state = WIN
					candidate.score = self.quota
					self.finished = True
					self.winner.append(candidate)
					return FINISHED
		# FINISHED if one of the candidates reached quota.
		for candidate in self.candidates:
			if candidate.score >= self.quota:
				candidate.state = WIN
				candidate.score = self.quota
				self.finished = True
				self.winner.append(candidate)
				return FINISHED
		# Eliminate candidates with the lowest scores and check for ties
		else:
			self.eliminateLowestCandidates()
			self.checkTies()
			return STOP

	def runStepSenator(self):
		"""Runs one iteration of the senatorial race. This method does one of the following actions:
				1. Applies current_ballots, then returns CONTINUE.
				2. Handles the case when NUM_SENATORS of candidates are RUNNING or WIN, then returns FINISHED.
				3. Handles the case when there are NUM_SENATORS winners, then returns FINISHED.
				4. Make quota'd RUNNING candidates WIN, then returns CONTINUE.
				5. Eliminates candidates with the fewest score, then returns STOP.
			@parameter: None
			@return: STOP, CONTINUE, FINISHED (0, 1, 2)
			@error: ElectionError('There is a tie!')
		"""	
		if self.current_ballots:
			self.applyCurrentBallot()
			return CONTINUE
		if (len(self.current_winners) + len(self.current_runners)) <= NUM_SENATORS:
			self.current_runners.sort(key=lambda x: -1 * x.score)
			if self.current_runners[0].score >= self.quota:
				candidate = self.current_runners.pop(0)
				self.makeCandidateWin(candidate)
				return CONTINUE				# This allows people to redistribute the votes of quota'd candidate
			self.winner = self.current_winners + self.current_runners	# Why do we need this code?
			self.finished = True
			return FINISHED
		if len(self.current_winners) == NUM_SENATORS:
			self.winner = self.current_winners
			self.finished = True
			return FINISHED

		self.current_runners.sort(key=lambda x: x.score)
		top_candidate = self.current_runners[-1]
		top_score = top_candidate.score

		if top_score >= self.quota:	# Determining quota'd candidates for this round
			self.current_runners.sort(key=lambda x: -1 * x.score)
			while self.current_runners[0].score >= self.quota and len(self.current_winners) < NUM_SENATORS:
				candidate = self.current_runners.pop(0)
				self.makeCandidateWin(candidate)
			return CONTINUE
		else:			# Eliminating lowest candidate
			last_candidate = self.current_runners.pop(0)
			self.current_ballots += last_candidate.ballots
			last_candidate.state = LOSE
			# Take out all tied candidates
			while True:
				if self.current_runners[0].score == last_candidate.score:
					curr_candidate = self.current_runners.pop(0)
					self.current_ballots += curr_candidate.ballots
					curr_candidate.state = LOSE
				else:
					break
			shuffle(self.current_ballots)		# Why shuffle?
			return STOP

	def makeCandidateWin(self, candidate):
		candidate.state = WIN
		self.current_winners.append(candidate)
		for ballot in candidate.ballots:
			ballot.value = ballot.value * float(candidate.score - self.quota)/candidate.score
			self.current_ballots.append(ballot)
		candidate.score = self.quota
		candidate.quotaPlace = NUM_SENATORS - len(self.current_winners) + 1

	def applyCurrentBallot(self):
		"""Count current ballot. If candidate loses, redistribute ballots.
			@parameter: None
			@return: None

			>>> ballot1 = Ballot({2: [101]})
			>>> ballot2 = Ballot({2: [101]})
			>>> tyrion = Candidate(101, 'Tyrion', 2, 'Lanister')
			>>> ned = Candidate(102, 'Ned', 2, 'Stark')
			>>> race = Race(None, 2, [tyrion, ned], [ballot1, ballot2])
		"""
		ballot = self.current_ballots.pop(0)
		if ballot.candidate and ballot.candidate.state == LOSE:
			ballot.candidate.score -= ballot.value
		self.applyBallot(ballot)


	def applyBallot(self, ballot):
		"""Increment a candidates score, and pop his number off the vote. Does NOT affect the state of a candidate.
			@parameters: Ballot object
			@error: Position not found
					Candidate not found

			>>> ballot1 = Ballot({1: [101]})
			>>> ballot2 = Ballot({1: [101]})
			>>> tyrion = Candidate(101, 'Tyrion', 1, 'Lanister')
			>>> ned = Candidate(102, 'Ned', 1, 'Stark')
			>>> race = Race(None, 1, [tyrion, ned], [ballot1, ballot2])
			>>> race.candidates[0].score
			0
			>>> race.candidates[1].score
			0
			>>> race.applyBallot(ballot1)
			True
			>>> race.candidates[0].score
			1
			>>> race.candidates[1].score
			0
			>>> race.applyBallot(ballot2)
			True
			>>> race.candidates[0].score
			2
			>>> race.applyBallot(ballot1)
			False
			>>> race.candidates[0].score
			2
			>>> race.candidates[1].score
			0

		"""
		if self.position not in ballot.votes.keys():
			raise ElectionError("Position not found in ballot!")
		vote = ballot.votes[self.position]		# Vote = list of preference of a single Ballot object

		while True:
			if not vote:
				self.spentBallots += ballot.value		# What is spentBallots? Why add ballot.value?
				return False
			candidate_num = int(vote.pop(0))			# Pop off the current top candidate
			if candidate_num not in self.numToCandidate.keys():
				raise ElectionError("Candidate " + str(candidate_num) + " not found!")
			if self.numToCandidate[candidate_num].state == RUNNING:		# If candidate is reached quota or was eliminated, redue the loop
				break

		candidate = self.numToCandidate[candidate_num]
		candidate.score += ballot.value
		candidate.ballots.append(ballot)
		ballot.candidate = candidate
		return True

	def eliminateLowestCandidates(self):
		"""Eliminates the candidates with the lowest score by changing candidate's state to LOSE. Note that this does not mutate the
			race.candidates array. BETTER NAME is makeLoseLowestCandidates.
			@parameter: None
			@return: list of eliminated candidate's number (int)

			>>> ballot1 = Ballot({2: [101]})
			>>> ballot2 = Ballot({2: [101]})
			>>> tyrion = Candidate(101, 'Tyrion', 2, 'Lanister')
			>>> ned = Candidate(102, 'Ned', 2, 'Stark')
			>>> race = Race(None, 2, [tyrion, ned], [ballot1, ballot2])
			>>> race.runStepExecutives()
			1
			>>> race.eliminateLowestCandidates()
			[102]
			>>> race.numOfRunners()
			1
			>>> len(race.candidates)
			2
			>>> race = Race(None, 2, [tyrion, ned], [ballot1, ballot2])
			>>> ned.state = RUNNING
			>>> ned.score = 1
			>>> race.eliminateLowestCandidates()
			[102, 101]
		"""
		removedCandidatesNum = []
		self.candidates.sort(key=lambda x: -1 * x.score) 		# Sorts candidates from lowest score to highest score
		worst_score = sys.maxint
		for candidate in reversed(self.candidates):
			if candidate.state == RUNNING and candidate.score <= worst_score:
				self.current_ballots += candidate.ballots
				candidate.state = LOSE
				removedCandidatesNum.append(candidate.number)
				worst_score = candidate.score
		return removedCandidatesNum

	def checkTies(self):
		"""Checks if there is a tie. For an executive race, 
			@parameter: None
			@returns: None
			@error: ElectionError('There is a tie!')

			>>> ballot1 = Ballot({2: [101]})
			>>> ballot2 = Ballot({2: [102]})
			>>> tyrion = Candidate(101, 'Tyrion', 2, 'Lanister')
			>>> ned = Candidate(102, 'Ned', 2, 'Stark')
			>>> race = Race(None, 2, [tyrion, ned], [ballot1, ballot2])
			>>> race.runStepExecutives() 		# Applies ballot1
			1
			>>> race.runStepExecutives() 		# Applies ballot2
			1
			>>> race.runStepExecutives() 		# Deletes the lowest (only) two candidates, and raises ElectionError
			Traceback (most recent call last):
			ElectionError: 'There is a tie!'
			>>> race.numOfRunners()
			0
		"""
		if self.position != SENATOR:
			if self.numOfRunners() == 0:
				raise ElectionError('There is a tie!')
		else:
			if self.numOfRunners() < NUM_SENATORS:
				raise ElectionError('There is a tie!')



	# def removeCandidate(candidate_id):
	# 	"""Removes the candidate with the candidate_id (str)
	# 		@parameter: candidate_id (str)
	# 		@return: candidate_id (str) or False
	# 		@error: ValueError when input is not str

	# 	>>> 
	# 	"""
	# 	if type(candidate_id) != str:
	# 		raise ValueError("Input must be a str.")



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
	

