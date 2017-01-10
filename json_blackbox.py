import json
import re
import hashlib
from autosub.autosub2 import autosub2

def get_times(keys,file_pwd,transcript_timed_dir,key_time_map_dir):
	transcript_timed_file = open(transcript_timed_dir,'r')
	transcript_timed = json.load(transcript_timed_file)
	transcript_timed_file.close()
	key_time_map_file = open(key_time_map_dir,'r')
	key_time_map = json.load(key_time_map_file)
	key_time_map_file.close()
	key_ranges_map = {}
	keys = list(map(lambda x: x.lower(), keys))
	back_up_keys = keys
	for k in keys:
		if key_time_map.has_key(k):
			keys.remove(k)
	for k in keys:
		dic = {k: []}
		key_ranges_map.update(dic)
	for i in transcript_timed:
		for k in keys:
			if re.search(k, i["content"] , re.IGNORECASE):
				start = i["start"]
				end = i["end"]
				key_ranges_map[k].append([start,end])
	for k in keys:
		ranges = key_ranges_map[k]
		time = autosub2(file_pwd,ranges,k)
		key_time_map.update({k: time})

	key_time_map_file = open(key_time_map_dir,'w')		
	key_time_map_file.write(json.dumps(key_time_map))
	key_time_map_file.close()

get_times(['work','start'],'/Users/n0where/Desktop/DFA_01.flac','./transcripts/DFA.json','./transcripts/test2.json')