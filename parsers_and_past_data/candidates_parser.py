# Parses candidates2013raw.txt to candidates2013.json
# UNIX command: python2.7 candidate_parser.py [text_file.txt] [filename.json]

import sys, json
from collections import *

# Dictionary for translating candidate positions (eg. "Academic VP" -> "academic_vp")
CANDIDATE_POSITIONS = { "Academic VP": "academic_vp", "Executive VP": "executive_vp", "External VP": "external_vp", "President": "president", "Senator": "senator", "Student Advocate": "student_advocate"}

candidates = defaultdict(list)
new_file = open(str(sys.argv[2]), 'w')

with open(str(sys.argv[1]), 'rU') as f:
	while True:
		line = f.readline()
		if not line:
			break
		line = line.split("\t")
		candidate = {}
		candidate['number'] = line[0]
		candidate['name'] = line[1][1:-1].replace("\\", "")
		candidate['party'] = line[3][1:-1]
		position = CANDIDATE_POSITIONS[line[4][1:-2]]
		
		candidates[position].append(candidate)
# print(json.dumps(candidates, sort_keys=True, indent=4, separators=(',', ': ')))
json.dump(candidates, new_file, sort_keys=True, indent=4, separators=(',', ': '))