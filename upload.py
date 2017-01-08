from bottle import route, run, template, view, redirect, post, request
import pymssql

# @route('/upload/upload_data')
# def upload_data():
# 	conn = pymssql.connect(server='asq-bottle.database.windows.net', user='ruizheli@asq-bottle.database.windows.net', password='Fzj990418.', database='asq-bottle')
# 	cursor = conn.cursor()
# 	#cursor.execute('INSERT INTO dbo.asq_file_data (title, author) VALUES ('Lecture', 'Anwar')')
# 	cursor.execute('INSERT INTO [dbo].[asq_file_data] ([title] ,[author],[tags],[description],[subject],[format],[file],[transcript_timed],[key_time_map]) VALUES (N\'testTitle\',N\'testAuthor\',N\'testTags\',N\'testDescription\',N\'CS\',N\'video\',convert(varbinary, \'testFile\'),convert(varbinary, \'testTranscript\'),convert(varbinary, \'testMap\'))')

# 	conn.commit()
# 	conn.close()

# 	redirect('/upload/upload_success')

@route('/upload/upload_data', method='POST')
def upload_data():
	print("connecting")
	servername = 'asq-bottle.database.windows.net'
	databasename = 'asq-bottle'
	username = 'ruizheli@asq-bottle.database.windows.net'
	pwd = 'Fzj990418.'
	#for mac
	# driver = '{/usr/local/lib/libtdsodbc.so}'
	# # driver= '{ODBC Driver 13 for SQL Server}'
	# cnxn = pyodbc.connect('DRIVER='+driver+';TDS_VERSION=8.0;PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
	# print("connected")
	# cursor = cnxn.cursor()

	# title = request.forms.get('title')
	# author = request.forms.get('author')
	# cursor.execute('INSERT INTO [dbo].[asq_file_data] ([title] ,[author],[tags],[description],[subject],[format],[file],[transcript_timed],[key_time_map]) VALUES (N\'' + title + '\',N\'' + author + '\',N\'testTags\',N\'testDescription\',N\'CS\',N\'video\',convert(varbinary, \'testFile\'),convert(varbinary, \'testTranscript\'),convert(varbinary, \'testMap\'))')



	title = request.forms.get('title')
	author = request.forms.get('author')

	conn = pymssql.connect(server=servername,user=username,password=pwd,database=databasename)
	cursor = conn.cursor()
	#cursor.execute('INSERT INTO dbo.asq_file_data (title, author) VALUES ('Lecture', 'Anwar')')
	cursor.execute('INSERT INTO [dbo].[asq_file_data] ([title] ,[author],[tags],[description],[subject],[format],[file],[transcript_timed],[key_time_map]) VALUES (N\'' + title + '\',N\'' + author + '\',N\'testTags\',N\'testDescription\',N\'CS\',N\'video\',convert(varbinary, \'testFile\'),convert(varbinary, \'testTranscript\'),convert(varbinary, \'testMap\'))')

	conn.commit()
	conn.close()

	redirect('/upload/upload_success')
