from tf_weighting import Tf_Weighting


class Augmented_Tf_Weighting(Tf_Weighting):
    
    def getTfWeightingForDocument(self, word, doc, docMatrix):
        
        if doc in docMatrix.dataDict[word]:
            return 0.5 + (docMatrix.dataDict[word][doc] * 0.5) / docMatrix.maxTermFreq
        return 0.5 / docMatrix.maxTermFreq
                         
                          
    def getTfWeightingForQuery(self, word, dataDict, maxFreq):
        return ((dataDict[word] * 0.5) / maxFreq) + 0.5
                 
    def ignoreZeroes(self):
        return False