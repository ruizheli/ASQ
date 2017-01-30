import subprocess
from whoosh.index import create_in
from whoosh.fields import *
import os
import codecs
from whoosh.qparser import QueryParser
import whoosh.index as index
import json
from autosub.autosub import autosub
from azure.storage.blob import AppendBlobService

vedio_formats = ['mp4','avi','wmv','mov'] # 1
audio_formats = ['wav','flac','mp3','aiff'] # 2

def file_upload(file_pwd, append_blob_service):
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
	transcript = autosub(file_pwd, format="json")
	print "Generated data structure: \n"
	whoosh_indexing(file_name,file_pwd,transcript, append_blob_service)
	return transcript

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

def whoosh_indexing(file_name,file_pwd,transcript, append_blob_service):
	transcripts_timed = json.loads(transcript)
	transcripts_content = ''
	for i in transcripts_timed:
		transcripts_content = transcripts_content + ' ' + i['content']
	# Whoosh the search engine
	schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
	if not os.path.exists("temp_index"):
	    os.mkdir("temp_index")
	ix = index.create_in("temp_index", schema)
	# ix = index.open_dir("temp_index")
	writer = ix.writer()
	writer.update_document(title=file_name.decode('utf-8'), path=file_pwd.decode('utf-8'), content=transcripts_content.decode('utf-8'))
	writer.commit()

	# for filename in os.listdir('temp_index'):
	#     root, ext = os.path.splitext(filename)
	#     if root.startswith('MAIN_') and ext == '.seg':
	#         file = filename

	# print(os.path.join('temp_index', file))
	# append_blob_service.create_blob('search-file', file)
	# append_blob_service.append_blob_from_path(
	# 	'search-file',
	# 	file,
	# 	os.path.join('temp_index', file)
	# )
	print("Written")

# throw formatError
def file_format(file_type):
	if file_type in vedio_formats:
		return 1;
	elif file_type in audio_formats:
		return 2
	else: 
		return 3

