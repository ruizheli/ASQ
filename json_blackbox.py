import json
import re
import hashlib

def get_times(keys,transcript_timed_dir,key_time_map_dir):
	transcript_timed_file = open(transcript_timed_dir,'r')
	transcript_timed = json.load(transcript_timed_file)
	transcript_timed_file.close()
	key_time_map_file = open(key_time_map_dir,'r')
	key_time_map = json.load(key_time_map_file)
	key_time_map_file.close()
	keys = list(map(lambda x: x.lower(), keys))
	for k in keys:
		if key_time_map.has_key(k):
			keys.remove(k)
	for k in keys:
		dic = {k: []}
		key_time_map.update(dic)
	for i in transcript_timed:
		for k in keys:
			if re.search(k, i["content"] , re.IGNORECASE):
				start = i["start"]
				end = i["end"]
				key_time_map[k].append([start,end])
	key_time_map_file = open(key_time_map_dir,'w')		
	key_time_map_file.write(json.dumps(key_time_map))
	key_time_map_file.close()

get_times(['work','start'], './transcripts/DFA.json','./transcripts/test2.json')