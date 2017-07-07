import math

#used to represent a document as a vector
class DocumentVector:

    def __init__(self):
        self.values = {}
        self.size = 0;
             
    def __iter__(self):
        for val in self.values:
            yield (val, self.values[val])

    def addValue(self, word, value):
        self.values[word] = value

    #returns all the tf.idf values
    def wordSet(self):
        return set(self.values.keys())

    #call this method after we have finished adding to the document vector
    #to compute the count. Saves us doing the calculation each time for data
    #that doesn't change
    def finalize(self):
        sumOf = 0
        for val in self.values:
            sumOf += math.pow(self.values[val], 2)
        
        self.size = math.sqrt(sumOf)   
        
    #returns the magnitude of the vector
    def sizeOfDocumentVector(self):
        return self.size