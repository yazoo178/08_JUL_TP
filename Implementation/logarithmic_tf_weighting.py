from tf_weighting import Tf_Weighting
import math

class Logarithmic_Tf_Weighting(Tf_Weighting):
	
	def getTfWeightingForDocument(self, word, doc, docMatrix):
		return math.log10(docMatrix.dataDict[word][doc])  + 1
	
	def getTfWeightingForQuery(self, word, dataDict, maxFreq):
		return math.log10(dataDict[word]) + 1