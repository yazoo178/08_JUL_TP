import re

class BooleanQueryModel:

    BooleanQueryRegex = "(([A-z]+)( (AND|OR) ([A-z]+))*)"
        

    def __init__(self, _invertedIndex):
        self.invertedIndex = _invertedIndex;
        self.querySet = {"OR", "AND"}
       
    #performs a simple boolean query on documents 
    def query(self, queryString, useStremming):
        from nltk.stem import PorterStemmer
        stemmer = PorterStemmer()
        resultIds = set()
        lastCombinator = ""
        
        for item in re.split("\W+", queryString):
            if item in self.querySet:
                lastCombinator = item
                continue
            
            if useStremming:
                item = stemmer.stem(item)
                
            wordSet = self.getPostingsForWord(item)
            
            if lastCombinator == "OR":
                resultIds.update(wordSet)
            elif lastCombinator == "AND":
                resultIds.intersection_update(wordSet)
            else:
                resultIds.update(wordSet)

        return resultIds
        
        
    def getPostingsForWord(self, word):
        tmpResults = set()
        if word in self.invertedIndex.dataDict:
            for doc in self.invertedIndex.dataDict[word]:
                tmpResults.add(doc)
        return tmpResults
        