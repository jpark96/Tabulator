import unittest
from Tabulator import *
from constants import *
from Race import *

class raceTest(unittest.TestCase):
	def setUp(self):
		candidate = Candidate(1, "Alice", SENATOR, "D")
		self.candidate_list = [candidate]
		self.race = Race(SENATOR, self.candidate_list, [])

	# def testRace(self):
	# 	candidate = Candidate(1, "Alice", SENATOR, "D")
	# 	self.assertTrue(self.race.candidates == [candidate])
	# 	self.assertTrue(self.race.candidateVotes[candidate.number] == 0)

	# def testApplyBallot(self):
	# 	test_race = Race(SENATOR, self.candidate_list, [])

	# 	# Create a ballot with one vote for Senator candidate #1.
	# 	senatorVotes = [1]
	# 	votes = {SENATOR: senatorVotes}
	# 	ballot = Ballot(votes)

	# 	# Apply the ballot and check candidate #1 has 1 vote
	# 	test_race.applyBallot(ballot);
	# 	self.assertTrue(test_race.candidateVotes[1] == 1)

	
	# def testNoCandidate(self):
	# 	test_race = Race(SENATOR, self.candidate_list, [])

	# 	senatorVotes = [1,2]
	# 	votes = {SENATOR: senatorVotes}
	# 	ballot = Ballot(votes)

	# 	self.assertRaises(ElectionError, test_race.applyBallot, ballot)

	# def testApplyBallotExecutive(self):
	# 	election = Election()
	# 	election.loadBallotsFromJSONFile("sample_votes.json")
	# 	election.loadCandidatesFromJSONFile("sample_candidates.json")
	# 	self.assertTrue(election.tally(PRESIDENT).score == 3)

	# def testExecutiveCandidates2013(self):
	# 	election = Election()
	# 	election.loadBallotsFromJSONFile("ballots.json")
	# 	election.loadCandidatesFromJSONFile("candidates2013.json")
	# 	for position in POSITIONS:
	# 		if position != SENATOR:
	# 			print(election.tally(position))

	def testSenators2013(self):
		election = Election()
		election.loadBallotsFromJSONFile("ballots.json")
		election.loadCandidatesFromJSONFile("candidates2013.json")
		winners = election.tally(SENATOR)
		# winners.sort(key=lambda x: -1 * x.score)
		for winner in winners:
			print(winner)

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

		firstVote = election.ballots[0];
		self.assertTrue(firstVote.votes[SENATOR] == [30,31,32])
		self.assertTrue(firstVote.votes[STUDENT_ADVOCATE] == [25,26,27,28])
		fourthVote = election.ballots[3];
		self.assertTrue(fourthVote.votes[1] == [])

		election.loadBallotsFromJSONFile("ballots.json")

	def testLoadCandidatesFromJSON(self):
		election = Election()
		expected_senator = Candidate(30, "Alton", SENATOR, "D")
		election.loadCandidatesFromJSONFile("sample_candidates.json")
		self.assertTrue(election.candidates[SENATOR][0] == expected_senator)

		expected_president = Candidate(1, "Yun", PRESIDENT, "L")
		self.assertTrue(election.candidates[PRESIDENT][0] == expected_president)

		expected_evp = Candidate(16, "Amanda", EXTERNAL_VP, "L")
		self.assertTrue(election.candidates[EXTERNAL_VP][1] == expected_evp)

	# def testAbsoluteTally(self):	
	# 	election = Election()
	# 	election.loadBallotsFromJSONFile("sample_votes.json")

	# 	election.loadCandidatesFromJSONFile("sample_candidates.json")

	# 	candidate_result, score = election.tally(SENATOR)
	# 	expected_senator = Candidate(30, "Alton", SENATOR, "D")
	# 	self.assertTrue(candidate_result[0] == expected_senator)
	# 	self.assertTrue(score[0] == 3)

	# 	candidate_result, score = election.tally(STUDENT_ADVOCATE)
	# 	expected = Candidate(25, "Steve", STUDENT_ADVOCATE, "L")
	# 	self.assertTrue(candidate_result[1] == expected)
	# 	self.assertTrue(score[1] == 1)

class candidateTest(unittest.TestCase):
	def testCandidate(self):
		candidate = Candidate(1, "Alice", SENATOR, "D")
		self.assertTrue(candidate.name == "Alice")
		self.assertTrue(candidate.number == 1)
		self.assertTrue(candidate.position == SENATOR)
		self.assertTrue(candidate.party == "D")

def main():
	unittest.main()

if __name__ == "__main__":
	main()

