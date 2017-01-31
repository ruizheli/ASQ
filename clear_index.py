from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import whoosh.index as index

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
index.create_in("temp_index", schema)
