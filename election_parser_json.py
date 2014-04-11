#############################################################
#					election_parser.py						#
#			  Created by: Alton Zheng & Yun Park			#
#			   Copyright Elections Council 2013				#
#############################################################

import csv, sys, json

count = 0
voter_id = '0'

new_file = open(str(sys.argv[2]), 'w')

def get_votes(key):
	l = list(sorted(voter_data[key].iteritems()))
	l = [item[1] for item in l]
	return l

#open csv file
output = {}
output["ballots"] = []
with open(str(sys.argv[1]), 'rU') as f:
	reader = csv.reader(f)
	voter_data = {}
	for row in reader:
		if voter_id != row[0]:
			#output voter line
			if count != 0:
				
				ballot = {}
				
				ballot["1"] = get_votes('senator')
				ballot["2"] = get_votes('aavp')
				ballot["3"] = get_votes('eavp')
				ballot["4"] = get_votes('evp')
				ballot["5"] = get_votes('sa')
				ballot["6"] = get_votes('president')

				output["ballots"].append(ballot)

			#initialization
			count += 1
			voter_id = row[0]
			voter_data['id'] = count
			voter_data['president'] = {}
			voter_data['evp'] = {}
			voter_data['eavp'] = {}
			voter_data['aavp'] = {}
			voter_data['sa'] = {}
			voter_data['senator'] = {}

		position = row[1]
		candidate_number = row[3]
		rank = row[10]

		if position == '1':
			voter_data['president'][rank] = candidate_number
		elif position == '2':
			voter_data['evp'][rank] = candidate_number
		elif position == '3':
			voter_data['eavp'][rank] = candidate_number
		elif position == '4':
			voter_data['aavp'][rank] = candidate_number
		elif position == '5':
			voter_data['sa'][rank] = candidate_number
		elif position == '6':
			voter_data['senator'][rank] = candidate_number

json.dump(output, new_file)