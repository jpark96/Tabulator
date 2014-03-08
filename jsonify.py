import sys, json
from collections import *
new_file = open(str(sys.argv[2]), 'w')
candidates = defaultdict(list)

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
		position = line[4][1:-2]
		
		candidates[position].append(candidate)
print(json.dumps(candidates, sort_keys=True, indent=4, separators=(',', ': ')))



