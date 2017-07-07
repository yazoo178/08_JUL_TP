from query import Query
from progress import printProgress

#used to represent more than one query
class Queries:

    def __init__(self, documents, _matrix, stops, stem, _tfWeighter, _idfType, onTheFly):
        self.matrix = _matrix
        self.queries = []
        for index, doc in enumerate(documents):
            printProgress(index + 1, len(documents), prefix = 'Computing tf.idf for queries:', suffix = 'Complete', barLength = 50)
            qu = Query(None, doc.docid, _matrix,_tfWeighter, _idfType, queryData=doc)
            qu.loadIndexFromCollection(stops, stem, onTheFly)
            self.queries.append(qu)

    def __iter__(self):
        for q in self.queries:
            yield q
            
    def __len__(self):
        return len(self.queries)