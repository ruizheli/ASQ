# NOTE: Currently pymssql fails on Azure, while pyodbc fails locally. USE pyodbc FOR DEPLOYING!!!
from bottle import route, run, template, view, redirect, post, request
import pyodbc
import pymssql
import pymongo
import base64
import datetime

from pprint import pprint

@route('/upload/upload_data', method='POST')
def upload_data():
	title = request.forms.get('title')
	author = request.forms.get('author')
	tags = request.forms.get('tags')
	description = request.forms.get('description')
	category = request.forms.get('category')
	file = request.files.get('file')

	print(request.files)
	print(file)
	print('Encoding as base64')
	file_content = base64.b64encode(file.file.read())
	print('Encoding finished')
	# print(file_content)

	uri = "mongodb://asq-bottle:UTH80Mqd47BP7RiEK11YKAGNtjvP8qXIqZQy8av7rDLUjE67u6Bn4rwykl9Z64PSD1N5qv74cLvrVf7Thg7Gog==@asq-bottle.documents.azure.com:10250/?ssl=true&ssl_cert_reqs=CERT_NONE"
	client = pymongo.MongoClient(uri)
	db = client['asq-bottle']
	asq_file_data = db['asq_file_data']

	post = {"title"			:	title,
			"author"		: 	author,
			"date"			: 	datetime.datetime.utcnow(),
	        "tags"			: 	tags,
	        "description"	: 	description,
	        "subject"		:	category,
	        "format"		:	"video",
	        "file"			:	file_content,
	        "transcript_timed"	: "transcript_timed",
	        "key_time_map"	:	"key_time_map"}

	post_id = asq_file_data.insert_one(post).inserted_id

	print(post_id)

	redirect('/upload/upload_success')
