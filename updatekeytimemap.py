import json
import re
import hashlib
import os
from azure.storage.blob import AppendBlobService

append_blob_service = AppendBlobService(account_name='asqdata', account_key='FB9fAfnEv1uokM0KZmEbC38EFpxBESFCJKboqQaxSysTudNsRsHTB0HHDv4eSqUV2RUUK7RR9WiplPn0C07LZw==')

def get_files(title):
	content = append_blob_service.get_blob_to_bytes(
		'transcript',
		title,
		max_connections=10
	)

	transcript_timed = json.loads(content.content)
	key_time_map_path = os.path.join('transcripts', title + '.json')
	key_time_map_file = open(key_time_map_path,'r')
	print(key_time_map_file)
	key_time_map = json.load(key_time_map_file)
	key_time_map_file.close()
	return (transcript_timed,key_time_map)

def get_times(keys, title):
	(transcript_timed,key_time_map) = get_files(title.split('.')[0])
	# key_ranges_map = {}
	print('get_times' + title)
	keys = list(map(lambda x: x.lower(), keys))
	# back_up_keys = keys
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
	# this is for more accurate time line
	# for k in keys:
	# 	ranges = key_ranges_map[k]
	# 	time = autosub2(file_pwd,ranges,k)
	# 	key_time_map.update({k: time})
	key_time_map_path = os.path.join('transcripts', title.split('.')[0] + '.json')
	key_time_map_file = open(key_time_map_path,'wb')
	key_time_map_file.write(json.dumps(key_time_map))
	key_time_map_file.close()

	return json.dumps(key_time_map)

def update_key_time_map(keys, title):
	get_times(keys, title)
