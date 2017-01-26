
import subprocess
from whoosh.index import create_in
from whoosh.fields import *
import os
import codecs
from whoosh.qparser import QueryParser
import whoosh.index as index
import json
from autosub.autosub import autosub
from autosub.autosub2 import autosub2

vedio_formats = ['mp4','avi','wmv','mov'] # 1
audio_formats = ['wav','flac','mp3','aiff'] # 2

def file_upload(file_pwd):
	regex = r"(.+)\/(.+)"
	if re.search(regex, file_pwd):
		match = re.search(regex, file_pwd)
		file_dir = match.group(1) + '/'
		file_name_and_type = match.group(2).lower() 
	else:
		raise fileNameError('fileNameError')
	regex = r"(.+)\.(.+)"
	if re.search(regex, file_name_and_type):
	    match = re.search(regex, file_name_and_type)
	    file_name = match.group(1)
	    file_type = match.group(2).lower()
	else: 
		raise fileNameError('fileNameError')
	transcripts_timed_pwd = file_dir + file_name + '.json'
	result = autosub(file_pwd, format="json")
	print "Generated data structure: \n"
	return result
	# whoosh_indexing(file_name,file_pwd,transcripts_timed_pwd)

# def autosubing(file_pwd,transcripts_timed_pwd,file_type):
# 	if not os.path.isfile(transcripts_timed_pwd):
# 		if file_format(file_type) == 1:	
# 			# command = "python ./autosub/autosub.py -F json -V %s" %(file_pwd)
# 			# command = "python ./autosub/autosub.py %s -F json" %(file_pwd)
# 			autosub(file_pwd, format="json")
# 		elif file_format(file_type) == 2:
# 			# command = "python ./autosub/autosub.py %s -F json" %(file_pwd)
# 			autosub(file_pwd, format="json")
# 		else:
# 			autosub(file_pwd, format="json")
# 		print "Autosubed"
# 	else: 
# 		print 'file has already been autosubed'

def whoosh_indexing(file_name,file_pwd,transcripts_timed_pwd):
	json_data = open(transcripts_timed_pwd)
	transcripts_timed = json.load(json_data)
	transcripts_content = ''
	for i in transcripts_timed:
		transcripts_content = transcripts_content + ' ' + i['content']
	# Whoosh the search engine
	schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
	if not os.path.exists("index"):
	    os.mkdir("index")
	ix = index.open_dir("index")
	writer = ix.writer()
	writer.update_document(title=file_name.decode('utf-8'), path=file_pwd.decode('utf-8'), content=transcripts_content.decode('utf-8'))
	writer.commit()
	print("Written")
	with ix.searcher() as searcher:
		query = QueryParser("content", ix.schema).parse("atom")
		results = searcher.search(query)
		for i in results:
			print(i)
	json_data.close()

# throw formatError
def file_format(file_type):
	if file_type in vedio_formats:
		return 1;
	elif file_type in audio_formats:
		return 2
	else: 
		return 3


dir1 = '/Users/n0where/GoogleDrive/WeixinBot/saved/voices/voice_2546547996039896197.mp3'
dir2 = '/Users/n0where/Desktop/DFA_01.flac'
dir3 = '/Users/n0where/GoogleDrive/ASQ/ASQ/transcripts/Chem101.mp4'
dir4 = '/Users/n0where/GoogleDrive/WeixinBot/saved/voices/voice_1089270824656503909.mp3'
dir5 = '/Users/n0where/GoogleDrive/WeixinBot/saved/voices/voice_8675834799709315495.mp3'
dir6 = '/Users/n0where/GoogleDrive/ASQ/ASQ/transcripts/Chem101.mp4'
dir7 = "/Users/ruoxili/GoogleDrive/ASQ/ASQ/transcripts/Atom.mp4"
print file_upload(dir7)

