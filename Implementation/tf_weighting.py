#Base class for tf weighting
#returns the natural tf value of a word in a given document
#as our system doesn't store 0 values these methods will only get called
#if the value word exists in the document/query. However changing/overriding
#the ignore zeroes method to False will cause the both methods to fire in anycase
class Tf_Weighting:

    def getTfWeightingForDocument(self, word, doc, docMatrix):
        return docMatrix.dataDict[word][doc]
	
    def getTfWeightingForQuery(self, word, dataDict, maxFreq):
        return dataDict[word]

    def ignoreZeroes(self):
        return True