from whoosh.qparser import QueryParser
import whoosh.index as index
from whoosh.fields import *

def searchStr(String):
	ix = index.open_dir("index")
	results = ["none"]
	with ix.searcher() as searcher:
		query = QueryParser("content", ix.schema).parse(String)
		results = searcher.search(query, limit = 20)
		for i in results:
			print(i)

searchStr("atom")