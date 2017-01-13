# NOTE: Currently pymssql fails on Azure, while pyodbc fails locally. USE pyodbc FOR DEPLOYING!!!
from bottle import route, run, template, view, redirect, post, request
import pyodbc
import pymssql
import pymongo
import base64
import time
import uuid
import re
from azure.storage.blob import AppendBlobService
from pprint import pprint

@route('/upload/upload_data', method='POST')
def upload_data():
	print('request received')
	title = request.forms.get('title')
	author = request.forms.get('author')
	tags = request.forms.get('tags')
	description = request.forms.get('description')
	category = request.forms.get('category')
	print('getting file')
	file = request.files.get('file')
	# File received. Direct to success
	# redirect('/upload/upload_success')
	print('encoding')
	file_content = base64.b64encode(file.file.read())
	print('encoding finished')
	media_file_name = str(uuid.uuid4())

	# Use MS-SQL to store file info
	server = 'tcp:asq-bottle.database.windows.net'
	database = 'asq-bottle'
	username = 'ruizheli@asq-bottle'
	password = 'Fzj990418.'
	driver= '{ODBC Driver 13 for SQL Server}'

	# pyodbc part, for deploying only
	conn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
	
	# pymssql part, for testing only
	# conn = pymssql.connect(server='asq-bottle.database.windows.net',user='ruizheli@asq-bottle.database.windows.net', password='Fzj990418.', database='asq-bottle')

	# logics for uploading
	cursor = conn.cursor()
	query = """INSERT INTO [dbo].[asq_file_data] ([title], [author], [tags], [description], [subject], [format], [file], [transcript_timed], [key_time_map]) VALUES (N\'%s\', N\'%s\', N\'%s\',N\'%s\', N\'%s\', N\'video\', N\'%s\', N\'testTranscript\', N\'testMap\')"""
	cursor.execute(query % (title, author, tags, description, category, media_file_name,))

	conn.commit()
	conn.close()

	# Using Azure append blob storage to store files
	append_blob_service = AppendBlobService(account_name='asq', account_key='N9gBpIgrR2qlaLVw/A9wHEQaUi6Yp4wR9rRZmTNwScsPm4lhT/uCLSMzKCOPwR/O0a8HMoDQv29qxwGt60XpFw==')
	print('slicing the file')
	splitted_file = re.findall('.{1,3500000}', file_content)
	print('slicing finished')

	append_blob_service.create_blob('media-file', media_file_name)
	print('total number of partitions: %s' % (str(len(splitted_file))))
	percentage_step = 100.0 / len(splitted_file)
	precent = 0.0
	for file_block in splitted_file: 
		append_blob_service.append_blob_from_text(
			'media-file',
			media_file_name,
			file_block
		)
		precent += percentage_step
		print(str(precent) + "%")

	return("upload_success")
