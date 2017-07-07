from progress import printProgress
import math

#used to return document-query simularity results
#with respect to themselves in vector space.
class VectorSpaceModel:
    
    def __init__(self, _documentMatrix):
        self.documentMatrix = _documentMatrix
        
        #we can optimize our on the fly output by using a cache for the query set
        #this is done by storing the magnitude of documents already seen for previous queries
        self.docCache = {}
        
    #returns the top N documents for a given query
    #ARG:query:The query object
    #ARG:n:Number of Documents
    #returns a top n result set
    def getTopNDocumentsForQuery(self, query, n):
        
        #create a result set
        results = {}

        #get possible candidates
        candidates = self.getCandidateSet(query)
       
        #loop through all possible candidates
        for doc in candidates:
            
            #dot product sum of document vector against query vector
            dotProduct = 0
            
            #get just the words that are in the query AND the document
            queryWords = query.vectorDoc.wordSet()
            docWords = self.documentMatrix.vectorDocs[doc].wordSet()
            queryWords.intersection_update(docWords)
            
            #loop through each word and sum up the product of the word's value in
            #the document and the query
            for word in queryWords:
                dotProduct += (self.documentMatrix.vectorDocs[doc].values[word] * query.vectorDoc.values[word])
                
            #compute the simularity. The size of the query vector is not going to affect the result as it's
            #constant for each document we loop through
            results[doc] = dotProduct / (self.documentMatrix.vectorDocs[doc].sizeOfDocumentVector() * query.vectorDoc.sizeOfDocumentVector())
            
        #sort the results high-to-low
        resultSet = sorted(results.items(), key=lambda x: x[1], reverse=True)
        
        #if the command line option -1 was set then
        #return an optimized set of results following a
        #jagged array format
        if n is -1:
            return self.getOptimizedOutput(resultSet)
          
        #else just return the top n results
        return resultSet[:n]
        
            
    #gets the optimized top results for a query
    #ARG:resultSet:a ranking set of queries to documents
    def getOptimizedOutput(self, resultSet):

        #loop the result set
        for index, item in enumerate(resultSet):
            #get the next item to see if it falls out of range
            nextItem = resultSet[index + 1]
            #using test data (see documentation) I was able to determine
            #using a 55% difference betwen the vector similarities produced
            #the best results
            percentOfValue = (item[1] / 100) * 55
            
            #check to see if the next item is within 55% of the next item
            #if it is not then end then break out of the loop
            #also ensure we always return atleast one document fora query               
            if item[1] - percentOfValue > nextItem[1]:
                if index == 0:
                    yield item    
                break
            elif index == 20:
                break
            else:
                yield item
	
    #gets the top n documents for the query without storing tf-idf weightings
    #ARG:n:Number of Documents
    #ARG:query:The query object
    #ARG:documentMatrix:index representer
    #returns a top n result set
    def topNDocumentsForQueryOnTheFly(self, query, n):
        
        #create a result set
        results = {}
        
        #to avoid looping through every possible document, just get the most relevant documents
        candidateDocs = set()
        
        #get magnitude of the query
        sizeOfQueryVector = self.getQueryMagnitude(query)
             
        #get possible document candidates
        candidateDocs = self.getCandidateSet(query)
           
        #go through all the candidate docs
        for candidate in candidateDocs:
            
            #dot product sum of document vector against query vector
            dotProduct = 0
            
            #if we have seen this document already, then we will have cached its magnitude
            if candidate in self.docCache:
                for word in query.dataDict:
                    
                    if word in self.documentMatrix.dataDict and candidate in self.documentMatrix.dataDict[word]:
                        #compute the idf weighting
                        idf = self.documentMatrix.inverseDocumentFreq(word) if self.documentMatrix.idfType == "t" else self.documentMatrix.probinverseDocumentFreq(word)
                    
                        #compute the tf.idf weighting of the document
                        tfIdfDoc = self.documentMatrix.tfWeighter.getTfWeightingForDocument(word, candidate, self.documentMatrix) * idf
                    
                        #get the tf.idf weighting for the query
                        tfIdfQuery = query.tfWeighter.getTfWeightingForQuery(word, query.dataDict, query.maxTermFreq) * idf
                    
                         #we only to do this sum if the word exists in both the query and the document
                        #else the resulting product will be 0
                        dotProduct += tfIdfDoc * tfIdfQuery
                    
                #add the weighting to our results
                results[candidate] = dotProduct / (self.docCache[candidate] * sizeOfQueryVector)
            
            else:

                #magnitude of document
                sizeOfDocVector = 0
                
                #go through each word in the current candidate document
                for word in self.getWordsForThisDoc(candidate, self.documentMatrix):
                    
                    #compute the idf weighting
                    idf = self.documentMatrix.inverseDocumentFreq(word) if self.documentMatrix.idfType == "t" else self.documentMatrix.probinverseDocumentFreq(word)
                    
                    #compute the tf.idf weighting of the document
                    tfIdfDoc = self.documentMatrix.tfWeighter.getTfWeightingForDocument(word, candidate, self.documentMatrix) * idf
    
                    #append to the size of the document vector
                    sizeOfDocVector += math.pow(tfIdfDoc, 2)
                    
                    #check if the the word is in the query
                    if word in query.dataDict:
                        
                        #get the tf.idf weighting for the query
                        tfIdfQuery = query.tfWeighter.getTfWeightingForQuery(word, query.dataDict, query.maxTermFreq) * idf  
                    
                        #we only to do this sum if the word exists in both the query and the document
                        #else the resulting product will be 0
                        dotProduct += tfIdfDoc * tfIdfQuery
                        
                #compute the magnitude of the document
                sizeOfDocVector = math.sqrt(sizeOfDocVector)
                
                #cache the document id alongside the magnitude
                self.docCache[candidate] = sizeOfDocVector
                
                #add the weighting to our results
                results[candidate] = dotProduct / (sizeOfDocVector * sizeOfQueryVector)

        #return just the top n documents
        resultSet = sorted(results.items(), key=lambda x: x[1], reverse=True)[:n]
                      
        #if the command line option -1 was set then
        #return an optimized set of results following a
        #jagged array format
        if n is -1:
            return self.getOptimizedOutput(resultSet)
          
        #else just return the top n results
        return resultSet[:n]              
	

    #gets the words for a given document
    #ARG:doc:doc id
    #ARG:documentMatrix:index representer	
    #returns a set of words	
    def getWordsForThisDoc(self, doc, documentMatrix):
        resultSet = set()
        for word in documentMatrix.dataDict:
            if doc in documentMatrix.dataDict[word]:
                resultSet.add(word)
                
        return resultSet
    
    #returns candidate documents for a given query
    #ARG:query:the given query
    #returns a candidate set of document ids
    def getCandidateSet(self, query):
        candidateDocs = set()
        
        #loop through each word in the query and check if it exists in our index
        #add possible candidate to our candidate set
        for word in query.dataDict:
            if word in self.documentMatrix.dataDict:
                for key in self.documentMatrix.dataDict[word]:
                    candidateDocs.add(key)
            
        return candidateDocs
        
    #gets the magnitude of a given query
    #ARG:query:the query to process
    #returns a scaler value
    def getQueryMagnitude(self, query):
        magnitude = 0
        for word in query.dataDict:
            if word in self.documentMatrix.dataDict:
                magnitude += math.pow(self.documentMatrix.inverseDocumentFreq(word) * query.tfWeighter.getTfWeightingForQuery(word, query.dataDict, query.maxTermFreq), 2)
                                            
        return math.sqrt(magnitude)
    
    
    
    
    