# NOTE: Currently pymssql fails on Azure, while pyodbc fails locally. USE pyodbc FOR DEPLOYING!!!
from bottle import route, run, template, view, redirect, post, request
import pymssql
import pymongo
import base64
import time
import uuid
import re
import sys
import tempfile
import os
import logging
import subprocess
from azure.storage.blob import AppendBlobService
from pprint import pprint
from maintest import file_upload
from multiprocessing import Process, Queue

append_blob_service = AppendBlobService(account_name='asqdata', account_key='FB9fAfnEv1uokM0KZmEbC38EFpxBESFCJKboqQaxSysTudNsRsHTB0HHDv4eSqUV2RUUK7RR9WiplPn0C07LZw==')
logger = logging.getLogger('asq')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

@route('/upload/upload_data', method='POST')
def upload_data():
	# try:
	if (request.forms.get('geturi') == 'true') :
		with open('containerSASToken.txt', 'r') as myfile:
			data = myfile.read().replace('\n', '')
		return data
	elif (request.forms.get('finished') != 'true') :
		SQLLoader(request.forms)
	elif (request.forms.get('finished') == 'true') :
		p = Process(target=fileProcessor, args=(request.forms,))
		p.start()

	# 	p = Process(target=SQLLoader, args=(request.forms,))
	# 	p.start()
	# elif (request.forms.get('finished') != 'true'):
	# 	p = Process(target=blobLoader, args=(request.forms,))
	# 	p.start()
	# elif (request.forms.get('finished') == 'true'):
	# 	p = Process(target=fileProcessor, args=(request.forms,))
	# 	p.start()
	# except UploadError:
		# print('upload error')
		# return("upload_fail")

def SQLLoader(form) :
	print('creating SQL entry')
	logger.info('creating SQL entry')
	title = request.forms.get('title')
	author = request.forms.get('author')
	tags = request.forms.get('tags')
	description = request.forms.get('description')
	category = request.forms.get('category')
	media_file_name = request.forms.get('fileName').split('.')[0]
	print(request.forms.get('fileName'))
	file_type = request.forms.get('fileName').split('.')[1]
	education = request.forms.get('school')
	course = request.forms.get('course')

	server = 'tcp:asq-file.database.windows.net'
	database = 'asq-file'
	username = 'ruizheli@asq-file'
	password = 'Fzj990418.'
	driver= '{ODBC Driver 13 for SQL Server}'

	# pyodbc part, for deploying only
	# conn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
	
	# pymssql part, for testing only
	conn = pymssql.connect(server='asq-file.database.windows.net',user='ruizheli@asq-file.database.windows.net', password='Fzj990418.', database='asq-file', tds_version='7.0')

	# logics for uploading
	cursor = conn.cursor()
	query = """INSERT INTO [dbo].[asq_file] ([title], [author], [tags], [description], [subject], [format], [file_name], [education], [course], [file_type]) VALUES (N\'%s\', N\'%s\', N\'%s\',N\'%s\', N\'%s\', N\'video\', N\'%s\', N\'%s\', N\'%s\', N\'%s\')"""
	cursor.execute(query % (title, author, tags, description, category, media_file_name, education, course, file_type, ))

	conn.commit()
	conn.close()

	print(media_file_name)
	logger.debug(media_file_name)

	print('finished SQL entry')
	logger.info('finished SQL entry')

def blobLoader(form) :
	print('loading blob entry')
	logger.info('loading blob entry')
	blob = base64.b64decode(request.forms.get('blob'))
	media_file_name = request.forms.get('fileName').split('.')[0]

	append_blob_service.append_blob_from_text(
		'media-file',
		media_file_name,
		blob
	)
	print(sys.getsizeof(blob))
	print('finished blob entry')
	logger.info('finished blob entry')

def fileProcessor(form) :
	print(form.get('fileName'))
	logger.debug('filename: ' + form.get('fileName'))
	media_file_name = form.get('fileName')
	if not os.path.exists("temp_index"):
		os.mkdir("temp_index")
	if not os.path.exists("temp"):
		os.mkdir("temp")
	if not os.path.exists("transcripts"):
		os.mkdir("transcripts")	
	if not os.path.exists("thumbnail"):
		os.mkdir("thumbnail")	
	content = append_blob_service.get_blob_to_bytes(
		'media-file',
		media_file_name.split('.')[0],
		max_connections=10
	)
	print(content)
	print(sys.getsizeof(content.content))
	temp_file_name = media_file_name
	temp_file_name = os.path.join('temp', temp_file_name)
	tf = open(temp_file_name, 'w+b')
	tf.write(content.content)
	tf.close()

	temp_key_file_name = os.path.join('transcripts', media_file_name.split('.')[0] + '.json')
	tf = open(temp_key_file_name, 'w+b')
	tf.write('{}')
	tf.close()

	input_file = temp_file_name
	temp_thumbnail = os.path.join('static', 'content', media_file_name.split('.')[0] + '.png')
	command = ["ffmpeg", "-i", input_file, "-ss", "00:00:03.000", "-vframes", "1", temp_thumbnail]
	subprocess.check_output(command)
	append_blob_service.create_blob('thumbnails', media_file_name.split('.')[0])
	f = open(temp_thumbnail, 'rb')
	f_binary = f.read()
	f.close()
	append_blob_service.append_blob_from_text(
		'thumbnails',
		media_file_name.split('.')[0],
		f_binary
	)

	cwd = os.getcwd()
	# index_file_name = os.path.join('temp_index', I_FILE_NAME)
	# index_file = open(index_file_name, 'w+b')
	# index_content = append_blob_service.get_blob_to_bytes(
	# 	'search-file',
	# 	I_FILE_NAME
	# )
	# index_file.write(index_content.content)
	# index_file.close()
	transcript = file_upload(os.path.join(cwd, temp_file_name), append_blob_service)
	append_blob_service.create_blob('transcript', media_file_name.split('.')[0])
	append_blob_service.append_blob_from_text(
		'transcript',
		media_file_name.split('.')[0],
		transcript
	)
	os.remove(os.path.join(cwd, temp_file_name))
	# os.remove(os.path.join(cwd, 'temp_index', I_FILE_NAME))

