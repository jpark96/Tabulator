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

	def testApplyBallot(self):
		test_race = Race(SENATOR, self.candidate_list)

		# Create a ballot with one vote for Senator candidate #1.
		senatorVotes = [1]
		votes = {SENATOR: senatorVotes}
		ballot = Ballot(votes)

		# Apply the ballot and check candidate #1 has 1 vote
		test_race.applyBallot(ballot);
		self.assertTrue(test_race.candidateVotes[1] == 1)
	
	def testNoCandidate(self):
		test_race = Race(SENATOR, self.candidate_list)

		senatorVotes = [1,2]
		votes = {SENATOR: senatorVotes}
		ballot = Ballot(votes)

		self.assertRaises(ElectionError, test_race.applyBallot, ballot)

class ballotTest(unittest.TestCase):
	def testBallot(self):
		senatorVotes = [1]
		votes = {SENATOR: senatorVotes}
		ballot = Ballot(votes)
		self.assertTrue(ballot.votes[SENATOR] == [1])

	def testNonexistantPosition(self):
		votes = {123123: [1]}
		self.assertRaises(BallotError, Ballot, votes)

class electionTest(unittest.TestCase):
	def testLoadBallotsFromJSON(self):
		election = Election()
		election.loadBallotsFromJSONFile("sample_votes.json")
		self.assertTrue(election.ballots != None)
		firstVote = election.ballots[0];
		self.assertTrue(firstVote.votes[SENATOR] == [1,2,3])
		self.assertTrue(firstVote.votes[STUDENT_ADVOCATE] == [8])
		fourthVote = election.ballots[3];
		self.assertTrue(fourthVote.votes[1] == [])
		
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

