import unittest
from Tabulator import *
from constants import *
from Race import *

class raceTest(unittest.TestCase):
	def setUp(self):
		candidate = Candidate(1, "Alice", SENATOR)
		self.candidate_list = [candidate]
		self.race = Race(SENATOR, self.candidate_list)

	def testRace(self):
		candidate = Candidate(1, "Alice", SENATOR)
		self.assertTrue(self.race.candidates == [candidate])
		self.assertTrue(self.race.candidateVotes[candidate.number] == 0)

	def testBallot(self):
		senatorVotes = [1]
		votes = {SENATOR: senatorVotes}
		ballot = Ballot(votes)
		self.assertTrue(ballot.votes[SENATOR] == [1])

	def testApplyBallot(self):
		test_race = Race(SENATOR, self.candidate_list)

		# Create a ballot with one vote for Senator candidate #1.
		senatorVotes = [1]
		votes = {SENATOR: senatorVotes}
		ballot = Ballot(votes)

		# Apply the ballot and check candidate #1 has 1 vote
		test_race.applyBallot(ballot);
		self.assertTrue(test_race.candidateVotes[1] == 1)

class candidateTest(unittest.TestCase):
	def testCandidate(self):
		candidate = Candidate(1, "Alice", SENATOR)
		self.assertTrue(candidate.name == "Alice")
		self.assertTrue(candidate.number == 1)
		self.assertTrue(candidate.position == SENATOR)

def main():
	unittest.main()

if __name__ == "__main__":
	main()

