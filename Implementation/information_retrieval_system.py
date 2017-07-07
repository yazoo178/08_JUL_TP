from progress import printProgress

#class used to represent our IR system
#command line options are passed in here
class InformationRetrievalSystem:
    
    def __init__(self, outputName, stem, stops, useExistingIndexFile, queryId, outputFileName, _tfWeighter, _idfType, _numDocs, _rr, _fly):
        self.outputName = outputName
        self.stem = stem
        self.stops = stops
        self.useExistingIndexFile = useExistingIndexFile
        self.queryId = queryId
        self.outputFileName = outputFileName
        self.tfWeighter = _tfWeighter
        self.idfType = _idfType
        self.numberOfDocs = _numDocs
        self.relevanceRanker = _rr
        self.onTheFly = _fly
    
    def Run(self, path):
        
        #use the supplied document reader
        from read_documents import ReadDocuments
        
        #read the documents
        reader = ReadDocuments(path)
        
        #load the document data in a document matrix
        from document_matrix import DocumentMatrix
        self.matrix = DocumentMatrix(reader, self.tfWeighter, self.idfType)
        
        #If -I is checked then load the existing index file, using the output
        #path specified
        if self.useExistingIndexFile:
            self.matrix.loadIndexFromIndexFile(self.outputName, self.onTheFly)
        
        #otherwise load the data from the documents file and output
        #it to an index file
        else:
            self.matrix.loadIndexFromCollection(self.stops, self.stem, self.onTheFly)
            self.matrix.outputFileIndex(self.outputName)
            

        #check if we wish to rank a single query
        if self.queryId != -1:
            
            #create a new query object
            from query import Query
            query = Query(ReadDocuments("queries.txt"), self.queryId, self.matrix, self.tfWeighter, self.idfType)
            query.loadIndexFromCollection(self.stops, self.stem, self.onTheFly)
            
            fileWriter = open(self.outputFileName, 'w')
            
            #use rocchio relevance
            if self.relevanceRanker != -1:
                from rocchio_relevance import RocchioRelevance
                relevance = RocchioRelevance(self.matrix)
                results = relevance.beginRelevanceRank(query, self.relevanceRanker)
                
            #use vector space model to rank the output
            else:       
                from vector_space_model import VectorSpaceModel
                model = VectorSpaceModel(self.matrix)
                results = model.topNDocumentsForQueryOnTheFly(query, self.numberOfDocs) if self.onTheFly == 1 else model.getTopNDocumentsForQuery(query, self.numberOfDocs)

            #output the results to file
            for result in results:
                fileWriter.write(str(result[0]) + ":" + str(result[1]))
                fileWriter.write("\n")
        
        #else we wish to rank the full query set
        else:
            
            #create a new queries object. load each query from source file
            from queries import Queries
            queries = Queries(list(ReadDocuments("queries.txt")), self.matrix, self.stops, self.stem, self.tfWeighter, self.idfType, self.onTheFly)
              
            #use the vector space model
            from vector_space_model import VectorSpaceModel
            model = VectorSpaceModel(self.matrix)
            
            fileTest = open(self.outputFileName, 'w')
            
            #process each query and write each result to file
            for index, q in enumerate(queries):
                results = model.topNDocumentsForQueryOnTheFly(q, self.numberOfDocs) if self.onTheFly == 1 else model.getTopNDocumentsForQuery(q, self.numberOfDocs)
                printProgress(index + 1, len(queries), prefix = 'Generating results list:', suffix = 'Complete', barLength = 50)
                for result in results:
                    fileTest.write(str(q.qId) + " " + str(result[0]))
                    fileTest.write("\n")