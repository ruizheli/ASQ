from whoosh.index import create_in
from whoosh.fields import *
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
import os
if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)
writer = ix.writer()
writer.add_document(title=u"First document", path=u"/a", content=u"This is the first document we've added!")
writer.add_document(title=u"Second document", path=u"/b", content=u"The second one is even more interesting!")
import codecs
f = codecs.open("/Users/n0where/Desktop/DFA.srt","r","utf-8").read()
writer.add_document(title=u"DFA", path=u"/Users/n0where/Desktop/DFA.srt", content=f)
#writer.add_document(title=u"Third document", path=u"/b", content=u"The second one is even more interesting!The second one is even more interesting!The second one is even more interesting!The second one is even more interesting!The second one is even more interesting!The second one is even more interesting!The second one is even more interesting!The second one is even more interesting!The second one is even more interesting!The second one is even more interesting! star")
f = codecs.open("/Users/n0where/Desktop/dictionary.txt","r","utf-8").read()
writer.add_document(title=u"Dic", path=u"/Users/n0where/Desktop/Dic.srt", content=f)
writer.add_document(title=u"Dic2", path=u"/Users/n0where/Desktop/Dic.srt", content=f)
writer.add_document(title=u"Dic3", path=u"/Users/n0where/Desktop/Dic.srt", content=f)
writer.add_document(title=u"Dic4", path=u"/Users/n0where/Desktop/Dic.srt", content=f)
writer.add_document(title=u"Dic5", path=u"/Users/n0where/Desktop/Dic.srt", content=f)
writer.add_document(title=u"Dic6", path=u"/Users/n0where/Desktop/Dic.srt", content=f)
writer.add_document(title=u"Dic7", path=u"/Users/n0where/Desktop/Dic.srt", content=f)
writer.add_document(title=u"Dic8", path=u"/Users/n0where/Desktop/Dic.srt", content=f)
writer.add_document(title=u"Dic9", path=u"/Users/n0where/Desktop/Dic.srt", content=f)
writer.commit()
from whoosh.qparser import QueryParser
print("Written")
with ix.searcher() as searcher:
	query = QueryParser("content", ix.schema).parse("aaah")
	results = searcher.search(query)
	print(results[0])
	