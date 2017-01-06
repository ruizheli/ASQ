import json
file_dir = './transcripts/DFA_01.json'
with open(file_dir) as json_data:
    d = json.load(json_data)
    s = ''
    for i in d:
    	s = s + ' ' + i['content']
    print s