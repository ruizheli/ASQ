from whoosh.index import create_in
import whoosh.index as index
from whoosh.fields import *
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
import os
if not os.path.exists("index"):
    os.mkdir("index")
ix = index.open_dir("index")
from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
	query = QueryParser("content", ix.schema).parse("atom")
	results = searcher.search(query)
	print(results[0])
	