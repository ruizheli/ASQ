# NOTE: Currently pymssql fails on Azure, while pyodbc fails locally. USE pyodbc FOR DEPLOYING!!!
from bottle import route, run, template, view, redirect, post, request
import pyodbc
import pymssql
import pymongo
import base64
import time
import uuid
import re
import sys
from azure.storage.blob import AppendBlobService
from pprint import pprint

append_blob_service = AppendBlobService(account_name='asqdata', account_key='FB9fAfnEv1uokM0KZmEbC38EFpxBESFCJKboqQaxSysTudNsRsHTB0HHDv4eSqUV2RUUK7RR9WiplPn0C07LZw==')

@route('/upload/upload_data', method='POST')
def upload_data():
	# try:
	if (request.forms.get('reading') == 'false'):
		print('creating SQL entry')
		title = request.forms.get('title')
		author = request.forms.get('author')
		tags = request.forms.get('tags')
		description = request.forms.get('description')
		category = request.forms.get('category')
		media_file_name = request.forms.get('fileName')

		server = 'tcp:asq-file.database.windows.net'
		database = 'asq-file'
		username = 'ruizheli@asq-file'
		password = 'Fzj990418.'
		driver= '{ODBC Driver 13 for SQL Server}'

		# pyodbc part, for deploying only
		conn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
		
		# pymssql part, for testing only
		# conn = pymssql.connect(server='asq-file.database.windows.net',user='ruizheli@asq-file.database.windows.net', password='Fzj990418.', database='asq-file')

		# logics for uploading
		cursor = conn.cursor()
		query = """INSERT INTO [dbo].[asq_file] ([title], [author], [tags], [description], [subject], [format], [file]) VALUES (N\'%s\', N\'%s\', N\'%s\',N\'%s\', N\'%s\', N\'video\', N\'%s\')"""
		cursor.execute(query % (title, author, tags, description, category, media_file_name,))

		conn.commit()
		conn.close()

		append_blob_service.create_blob('media-file', media_file_name)
		print('finished SQL entry')
	elif (request.forms.get('finished') != 'true'):
		print('loading blob entry')
		blob = base64.b64decode(request.forms.get('blob'))
		media_file_name = request.forms.get('fileName')
		# print(blob)

		append_blob_service.append_blob_from_text(
			'media-file',
			media_file_name,
			blob
		)
		print(sys.getsizeof(blob))
		print('finished blob entry')
	# except UploadError:
		# print('upload error')
		# return("upload_fail")
