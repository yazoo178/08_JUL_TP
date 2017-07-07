import re, sys, math
from progress import printProgress


WordRegex = "'?\w[\w\d']*(?:-\w+)*'?"

#this class is used to represent a query
class Query:

    def __init__(self, _documentReader, queryId, _matrix, _tfWeighter, _idfType, queryData = None):
        self.vectorDoc = None
        self.dataDict = {} 
        self.matrix = _matrix
        self.qId = queryId
        self.tfWeighter = _tfWeighter
        self.idfType = _idfType
        
        if queryData == None: 
            for doc in _documentReader:
                if doc.docid == queryId:
                    self.query = doc
                    break
        
        else:
            self.query = queryData
        
    #loads the query into memory
    #applying any command line conditions accordingly I.E use stemming, stoplist etc
    def loadIndexFromCollection(self, stops, stem, onTheFly):
        for line in self.query.lines:
            for word in re.finditer(WordRegex, line):
                lowerWord = word.group().lower()
                if stem:
                    lowerWord = stem(lowerWord)
                if lowerWord not in stops:
                    if lowerWord in self.dataDict:
                        self.dataDict[lowerWord] += 1
                    else:
                        self.dataDict[lowerWord] = 1

        #we need to know the word with the maximum amount of occurences, capture that here
        self.maxTermFreq = self.dataDict[max(self.dataDict, key=lambda i: self.dataDict[i])]

        if onTheFly != 1:
            self.populateVectorIndex()
        

    #used to represent our query as a vector
    def populateVectorIndex(self):
        from document_vector import DocumentVector
        vect = DocumentVector()
        #loop through our words and generate tf.idf values for them
        for word in self.dataDict:
            #check if we wish to ignore 0s or if the word is contained in our main collection
            #(if it's not then we cannot estimate it's wright so don't generate a tf.idf value for it)
             if not self.tfWeighter.ignoreZeroes() or word in self.matrix.dataDict:
                if self.matrix.documentFreqOfWord(word) > 0:
                    tfValue = self.tfWeighter.getTfWeightingForQuery(word, self.dataDict, self.maxTermFreq)
                    idfValue = self.matrix.inverseDocumentFreq(word) if self.idfType == "t" else self.matrix.probinverseDocumentFreq(word)
                    vect.addValue(word, tfValue * idfValue)
                    
        vect.finalize()
        self.vectorDoc = vect

        
        
        
        
        
        
        
        
        
        
        
