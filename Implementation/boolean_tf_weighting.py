from tf_weighting import Tf_Weighting

#Boolean Model for tf weighting
#returns 1 if the word exists
#as our system doesn't store 0 values these methods will only get called
#if the value word exists in the document/query
class Boolean_Tf_Weighting(Tf_Weighting):
    
    def getTfWeightingForDocument(self, word, doc, docMatrix):
        return 1
                         
                          
    def getTfWeightingForQuery(self, word, dataDict, maxFreq):
        return 1
                 