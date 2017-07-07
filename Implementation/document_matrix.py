import re, math, concurrent.futures

WordRegex = "'?\w[\w\d']*(?:-\w+)*'?"
WordIndexFileRegex = "('?\w[\w\d']*(?:-\w+)*'?)(\t)({[0-9]+,[0-9]+})+"
TokenMatch = "{([0-9]+),([0-9]+)}"

#class used to represent our documents
#encapsulate the tokenized words
#the documents in which they occur
#and the count of each word
#this class also stores a vector
#representation of each document
class DocumentMatrix:

    def __init__(self, _documentReader,_tfWeighter, _idfType):
        
        #This is our inverted index
        #words->id->count
        self.dataDict = {}
        
		#Used for reading document collection
        self.documentReader = _documentReader
		
		#number of documents in the collection
        self.documentCount = 0
		
		#tf.idf vectors to store against against each document
		#this is optional and can be ignored by specifying the -F flag
        self.vectorDocs = {}
		
		#document ids
        self.docIds = set()
		
		#The most common term
        self.maxTermFreq = 0
		
		#abstract reference to a tf weighting
		#changes depending on the command-line parameters for -tf
        self.tfWeighter = _tfWeighter
		
		#idf type
        self.idfType = _idfType
	
    #This method will load the collection data from the specified documents
    #file. It then adds the data into dataDict
    #ARG:stops:An optional stop list of words to ignore
    #ARG:stem: the type of stemmer to use. 
    def loadIndexFromCollection(self, stops, stem, onTheFly):         
        for doc in self.documentReader:
            self.docIds.add(doc.docid)
            for line in doc.lines:
                for word in re.finditer(WordRegex, line):
                    lowerWord = word.group().lower()
                    if stem:
                        lowerWord = stem(lowerWord)
                    if lowerWord not in stops:
                        if lowerWord not in self.dataDict:
                            self.dataDict[lowerWord] = {}
                            self.dataDict[lowerWord][doc.docid] = 1
                        else:
                            if doc.docid in self.dataDict[lowerWord]:
                                self.dataDict[lowerWord][doc.docid] += 1
                            else:
                                self.dataDict[lowerWord][doc.docid] = 1

        self.computeDocumentCount()
        
		#if the on the fly flag was specified
		#then ignore this 
        if onTheFly != 1:
            self.populateVectorIndex()

    #Output the data in dataDict to a text file
    #ARG:outputFileName:the name of the file to output
    def outputFileIndex(self, outputFileName):
        file = open(outputFileName, 'w')
        
        for word in self.dataDict:
            file.write(word + "\t")
            for entry in self.dataDict[word]:
                file.write("{" + str(entry) + ',' +
                             str(self.dataDict[word][entry]) + "}")
            
            file.write('\n')
        file.close()
        
            
    #Loads exisiting data from an index file into dataDict
    #ARG:indexFile:the path of the index file
    def loadIndexFromIndexFile(self, indexFile, onTheFly):
        file = open(indexFile, 'r')
        data = file.read()

        for line in re.finditer(WordIndexFileRegex, data):
            word = line.group(1)
            self.dataDict[word] = {}
            for tokenMatcher in re.finditer(TokenMatch, line.group()):
                self.docIds.add(int(tokenMatcher.group(1)))
                self.dataDict[word][int(tokenMatcher.group(1))] = 0
                self.dataDict[word][int(tokenMatcher.group(1))] += int(tokenMatcher.group(2))
      
        self.computeDocumentCount()
		
        #if the on the fly flag was specified
		#then ignore this 
        if onTheFly != 1:
            self.populateVectorIndex()
                
    
    #works out the number of documents in collections
    #used for when we load an existing index file
    def computeDocumentCount(self):
        resultSet = set()
        for keyWord in self.dataDict:
            for keySet in self.dataDict[keyWord]:
                resultSet.add(keySet)
            if self.dataDict[keyWord][keySet] > self.maxTermFreq:
                self.maxTermFreq = self.dataDict[keyWord][keySet]
            
            
        self.documentCount = len(resultSet)
        
    
    #returns total number of documents in collection
    def totalDocumentsInCollection(self):
        return self.documentCount
        
    #returns how many documents contain a given word
    def documentFreqOfWord(self, word):
        if word in self.dataDict:
            return len(self.dataDict[word])
        else:
            return 0
        
    #returns the idf
    def inverseDocumentFreq(self, word):
        return math.log10(self.totalDocumentsInCollection() / self.documentFreqOfWord(word))
    
    def probinverseDocumentFreq(self, word):
        val= max(0, math.log((self.totalDocumentsInCollection() 
        - self.documentFreqOfWord(word))/self.documentFreqOfWord(word)))
        return val
        
    #populates tf.idf values for this dataset
    def populateVectorIndex(self):
        from document_vector import DocumentVector
        from progress import printProgress
        print(self.idfType)
        
        for docId in self.docIds:
            printProgress(docId, len(self.docIds), prefix = 'Computing tf.idf vectors:', suffix = 'Complete', barLength = 50)
            vect = DocumentVector()
            self.vectorDocs[docId] = vect
            for word in self.dataDict:
                if not self.tfWeighter.ignoreZeroes() or docId in self.dataDict[word]:
                    tfValue = self.tfWeighter.getTfWeightingForDocument(word, docId, self)
                    idfValue = self.inverseDocumentFreq(word) if self.idfType == "t" else self.probinverseDocumentFreq(word)
                    vect.addValue(word, tfValue * idfValue)
                    
            vect.finalize()
        










          
