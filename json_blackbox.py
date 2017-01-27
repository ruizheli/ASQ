import json
import re
import hashlib

def get_times(keys, transcript_timed_dir, key_time_map_dir, file_pwd = None,):
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
	# this is for more accurate time line
	# for k in keys:
	# 	ranges = key_ranges_map[k]
	# 	time = autosub2(file_pwd,ranges,k)
	# 	key_time_map.update({k: time})
	return json.dumps(key_ranges_map)

print get_times(['atom'],'./transcripts/Atom.json','./transcripts/Atom_keys.json')