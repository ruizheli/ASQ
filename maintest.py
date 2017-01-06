
import subprocess
from whoosh.index import create_in
from whoosh.fields import *
import os
import codecs
from whoosh.qparser import QueryParser

file_dir = "./transcripts/DFA_01.flac"
command = "python ./autosub/autosub.py %s -F json" %(file_dir)
subprocess.call(command, shell=True)	

import json
file_dir = './transcripts/DFA_01.json'
json_data = open(file_dir)
d = json.load(json_data)
s = ''
for i in d:
	s = s + ' ' + i['content']

# Whoosh the search engine
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)
writer = ix.writer()
writer.add_document(title=u"DFA", path=u"./transcripts/DFA_01.flac", content=s)
writer.commit()
print("Written")
with ix.searcher() as searcher:
	query = QueryParser("content", ix.schema).parse("video")
	results = searcher.search(query)
	print(results[0])


