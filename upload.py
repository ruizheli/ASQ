from bottle import route, run, template, view, redirect
import pymssql

@route('/upload/upload_data')
def upload_data():
	conn = pymssql.connect(server='asq-bottle.database.windows.net', user='ruizheli@asq-bottle.database.windows.net', password='Fzj990418.', database='asq-bottle')
	cursor = conn.cursor()
	#cursor.execute('INSERT INTO dbo.asq_file_data (title, author) VALUES ('Lecture', 'Anwar')')
	cursor.execute('INSERT INTO [dbo].[asq_file_data] ([title] ,[author],[tags],[description],[subject],[format],[file],[transcript_timed],[key_time_map]) VALUES (N\'testTitle\',N\'testAuthor\',N\'testTags\',N\'testDescription\',N\'CS\',N\'video\',convert(varbinary, \'testFile\'),convert(varbinary, \'testTranscript\'),convert(varbinary, \'testMap\'))')

	conn.commit()
	conn.close()

	redirect('/upload/upload_success')
