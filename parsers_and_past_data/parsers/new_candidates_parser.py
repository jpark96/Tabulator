# Parses candidates2015.txt to candidates2013.json
# UNIX command: python2.7 candidate_parser.py [text_file.txt] [filename.json]

import sys, json
from pprint import pprint
from collections import *

# Dictionary for translating candidate positions (eg. "Academic VP" -> "academic_vp")
CANDIDATE_POSITIONS = { "4": "academic_vp", "2": "executive_vp", "3": "external_vp", "1": "president", "6": "senator", "5": "student_advocate"}
CANDIDATE_PARTIES = {"1": "Independent", "2": "CalSERVE", "3": "Cooperative Movement Party (CMP)", "4": "SQUELCH!", "5": "Defend Affirmative Action Party (DAAP)", "6": "Student Action", "7": "BASED."}

candidates = defaultdict(list)
new_file = open(str(sys.argv[2]), 'w')

with open(str(sys.argv[1]), 'rU') as f:
	while True:
		line = f.readline()
		if not line:
			break
		array = line.split(",")
		candidate = {}
		candidate['number'] = array[1]

		first_name = array[6].decode('utf-8').strip().replace(u'\u2018','').replace(u'\u2019','')
		nickname = array[4].decode('utf-8').strip().replace(u'\u2018','').replace(u'\u2019','')
		middle_name = array[5].decode('utf-8').strip().replace(u'\u2018','').replace(u'\u2019','')
		last_name = array[3].decode('utf-8').strip().replace(u'\u2018','').replace(u'\u2019','')
		if nickname == 'NULL' and middle_name == 'NULL':
			name = first_name + " " + last_name
		elif middle_name == 'NULL':
			name = first_name + " \"" + nickname + "\" " + last_name
		elif nickname == 'NULL':
			name = first_name + " " + middle_name + " " + last_name
		else:
			name = first_name + " " + middle_name + " \"" + nickname + "\" " + last_name

		candidate['name'] = name
		candidate['party'] = CANDIDATE_PARTIES[array[2]]
		position = CANDIDATE_POSITIONS[array[0]]
		
		candidates[position].append(candidate)
# print(candidates)
# print(json.dumps(candidates, sort_keys=True, indent=4, separators=(',', ': ')))
json.dump(candidates, new_file, sort_keys=True, indent=4, separators=(',', ': '))
# json.dump(candidates, new_file, sort_keys=True, indent=4, separators=(',', ': '))