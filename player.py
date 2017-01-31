from bottle import route, run
import json
import pymssql
from azure.storage.blob import AppendBlobService
import os

append_blob_service = AppendBlobService(account_name='asqdata', account_key='FB9fAfnEv1uokM0KZmEbC38EFpxBESFCJKboqQaxSysTudNsRsHTB0HHDv4eSqUV2RUUK7RR9WiplPn0C07LZw==')

html1 = """<!DOCTYPE html>
<html>
<head>
	<title>"""
html2 = """</title>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	<link rel="stylesheet" type="text/css" href="/static/content/player.css">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

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
	
	
	<br>
	<div class="container">
		<h2>"""
html3 = """</h2>
		<br>
		<div class="row">
			<div class="col-md-3" id="left">
				<div class="concept">
					<h4>Concepts</h4>
					<ul>"""
html4 = """					</ul>
				</div>
				<hr>
				<div class="info">
					<p><strong>Author: </strong>"""

html5 = """</p>
					<p><strong>Course: </strong>"""
html6 = """</p>
					<p><strong>School: </strong>"""
html7 = """</p>
					<p><strong>Category: </strong>"""
html8 = """</p>
				</div>
			</div>
			<div class="col-md-9" id="right">
				<div class="video-container">
					<video width="100%" id="video" controls>
						<source src=\""""

html9 =						"""\" type="video/mp4">
						Your browser is currently not compatible, please use the newest version of Google Chrome.
					</video> 
				</div>
				<br>

				<div class="description">
					<p><strong>Description:</strong> <br>"""
html10 = """</p>
				</div>
				<br><br>
			</div>
		</div>
	</div>
	
	<br>
	<div class="footer">
		<footer>
			<div class="container">
				<h3>About</h3>
				<p>Parrot is brought to you by Ruizhe Li, Ruoxi Li, and Shengyi Chen</p>
<p>Parrot provides students with an efficient and streamlined way to refresh their memory with important concepts. Students can search for and upload lecture recordings, search any keyword or concept in the recordings, or discover new content to satisfy their intellectual needs. Parrot will take the student to that moment in the lecture with clinical precision. </p>			</div>  
		</footer>
	</div>

	<script src="/static/scripts/player.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
</body>

</html>"""

def get_files(title):
	key_time_map_file = open(os.path.join('transcripts', title.split('.')[0] + '.json'),'r')
	key_time_map = json.load(key_time_map_file)
	key_time_map_file.close()

	server = 'tcp:asq-file.database.windows.net'
	database = 'asq-file'
	username = 'ruizheli@asq-file'
	password = 'Fzj990418.'
	driver= '{ODBC Driver 13 for SQL Server}'

	# pyodbc part, for deploying only
	# conn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
	
	# pymssql part, for testing only
	conn = pymssql.connect(server='asq-file.database.windows.net',user='ruizheli@asq-file.database.windows.net', password='Fzj990418.', database='asq-file', tds_version='7.0')

	if not os.path.exists("temp"):
		os.mkdir("temp")
	content = append_blob_service.get_blob_to_bytes(
		'media-file',
		title.split('.')[0],
		max_connections=10
	)
	print(content)
	temp_file_name = title
	video_pwd = os.path.join('static', 'content', temp_file_name)
	tf = open(video_pwd, 'w+b')
	tf.write(content.content)
	tf.close()

	print(title)
	# logics for uploading
	cursor = conn.cursor()
	query = """SELECT * FROM [dbo].[asq_file] WHERE file_name=\'%s\'"""
	print(query % (str(title.split('.')[0]),))
	cursor.execute(query % (str(title.split('.')[0]),))
	result = cursor.next()

	title = str(result[0]) 
	tags = str(result[2]) 
	education = str(result[8]) 
	user = str(result[1]) 
	abstract = str(result[3]) 
	category = str(result[4]) 
	course = str(result[9]) 

	return (title, key_time_map,education,user,course,abstract,category, video_pwd)

@route('/player/<title:re:[\w\-]+>/<type:re:[\w\-]+>/<keys:re:((\w+\+)*)?\w+>')
def player(title, type, keys):
	s1 = """<li class="jump"><a href="#" onclick="jumpToTime("""
	s2 = """)">"""
	s3 = """</a></li>"""
	s_html = ""
	(title, key_time_map,education,user,course,abstract,category,video_pwd) = get_files(title + '.' + type)
	keys = keys.split("+")
	for k in keys:
		for i in key_time_map[k]:
			s = s1 + str(int(i[0])) +s2 + k + s3
			s_html += s
	html = html1 + title + html2 + title + html3 + s_html + html4 + user + html5 + course + html6 + education + html7 + category + html8 + "/" + video_pwd + html9 +abstract +html10
	return html
	
