from whoosh.qparser import QueryParser
import whoosh.index as index
from whoosh.fields import *
from bottle import route, run
from updatekeytimemap import update_key_time_map 
from azure.storage.blob import AppendBlobService
import pymssql
import re
import os

append_blob_service = AppendBlobService(account_name='asqdata', account_key='FB9fAfnEv1uokM0KZmEbC38EFpxBESFCJKboqQaxSysTudNsRsHTB0HHDv4eSqUV2RUUK7RR9WiplPn0C07LZw==')

html1 = """<!DOCTYPE html>
<html>
<head>
	<title>Search Results</title>
	<link rel="stylesheet" type="text/css" href="/static/content/search.css">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>

</head>
<body>
	<header>
		<div class="container">
			<div class="row">
				<div class="col-md-8">
					<h1><a href="/home" class="logo">Parrot</a></h1>
				</div>
				<div class="col-md-4">
					<div class="searchBox">
						<div class="input-group">
							<input type="text" class="form-control" id="search" placeholder="What do you want to learn?">
							<span class="input-group-btn">
								<button class="btn btn-default" id="go-btn" type="button" onclick="go_search();">Go</button>
							</span>
						</div>
					</div>
				</div>
			</div>
		</div>
	</header>
	
	<div class="container" id="result">
		<h2>Search Results</h2>
		<p><strong class="text-danger">"""
html2 = """</strong> results were found for the search for <strong class="text-danger">"""
html3 = """</strong></p><br>
		<section class="col-xs-12 col-sm-6 col-md-12" id="search_result">"""
html4 = """
	</div>
	
	<br>
	<div class="footer">
		<footer>
			<div class="container">
				<h3>About</h3>
				<p>Parrot is brought to you by Ruizhe Li, Ruoxi Li, and Shengyi Chen</p>
				<p>Parrot provides students with an efficient and streamlined way to refresh their memory with important concepts. Students can search for and upload lecture recordings, search any keyword or concept in the recordings, or discover new content to satisfy their intellectual needs. Parrot will take the student to that moment in the lecture with clinical precision. </p><p>
			<b>Disclaimer: All videos from this site are from YouTube. All rights belong to the original creaters/publishers of these videos. All videos are used for demo purpose only. The site is not intended for any commercial usage. The videos will be deleted immediately once the demo ends. </b>
			</p>			</div>  
		</footer>
	</div>

	<script src="/static/scripts/main.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
</body>

</html>"""

def get_info(title):
	fn = title
	server = 'tcp:asq-file.database.windows.net'
	database = 'asq-file'
	username = 'ruizheli@asq-file'
	password = 'Fzj990418.'
	driver= '{ODBC Driver 13 for SQL Server}'

	# pyodbc part, for deploying only
	# conn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
	
	# pymssql part, for testing only
	conn = pymssql.connect(server='asq-file.database.windows.net',user='ruizheli@asq-file.database.windows.net', password='Fzj990418.', database='asq-file', tds_version='7.0')

	print(title)
	# logics for uploading
	cursor = conn.cursor()
	query = """SELECT * FROM [dbo].[asq_file] WHERE file_name=\'%s\'"""
	print(query % (str(title),))
	cursor.execute(query % (str(title),))
	result = cursor.next()

	title = str(result[0].encode('utf-8')) 
	tags = str(result[2].encode('utf-8')) 
	education = str(result[8].encode('utf-8')) 
	user = str(result[1].encode('utf-8')) 
	abstract = str(result[3].encode('utf-8')) 

	content = append_blob_service.get_blob_to_bytes(
		'thumbnails',
		fn,
		max_connections=10
	)

	thumbnail = os.path.join('static', 'content', fn+'.png')
	tf = open(thumbnail, 'w+b')
	tf.write(content.content)
	tf.close()

	file_type = str(result[10]) 
	return (title,tags,education,user,abstract,thumbnail,file_type)

def results_html(title, String):
	fn = title
	(title,tags,education,user,abstract,thumbnail,file_type) = get_info(title)
	results_html1 = """<article class="row">
				<div class="col-xs-12 col-sm-12 col-md-3">
					<a href="#" class="thumbnail"><img src=\""""
	results_html2 = """\"alt="thumbnail"/></a>
				</div>
				<div class="col-xs-12 col-sm-12 col-md-2">
					<ul class="metadata">
						<li><i class="glyphicon glyphicon-tags"></i> <span class="meta">"""
	results_html3 = """</span></li><hr class="hidden_space">
						<li><i class="glyphicon glyphicon-education"></i> <span class="meta">"""
	results_html4 = """</span></li><hr class="hidden_space">
						<li><i class="glyphicon glyphicon-user"></i> <span class="meta">"""
	results_html5 = """</span></li>
					</ul>
				</div>
				<div class="col-xs-12 col-sm-12 col-md-7">
					<p style="font-size: 24px;"><a href="/player/"""
	results_html6 = """\">"""
	results_html7 = """</a></p>
					<p>"""
	results_html8 = """</p>
				</div>
			</article>"""

	# print(String)
	# print(title + "/" + String)
	results_html = results_html1 + thumbnail + results_html2 + tags + results_html3 + education + results_html4 + user + results_html5 + fn +  "/" + file_type.replace(" ", "") + "/" + String + results_html6 + title + results_html7 + abstract + results_html8
	return results_html

@route('/search/<String:re:([\w+\+]*)?\w+>')
def searchStr(String):
	ix = index.open_dir("temp_index")
	results = ["none"]
	results_num = 0
	r_html = ""
	keys = String.split("+")
	with ix.searcher() as searcher:
		query = QueryParser("content", ix.schema).parse(String)
		print query
		results = searcher.search(query, limit = 20)
		results_num = len(results)
		for i in results:
			update_key_time_map(keys,i["title"])
			r_html += results_html(i["title"].split('.')[0], String)
			r_html += """<hr>"""
	print "there are " + str(results_num) + " results"
	html = html1 + str(results_num) + html2 + String.replace('+', ' ') + html3 + r_html + html4 
	return html
