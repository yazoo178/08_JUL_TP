# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 17:05:21 2016

@author: Will
"""

#a class used for calculating relevance from feedback
#uses the rocchio relevance algorithem
#https://en.wikipedia.org/wiki/Rocchio_algorithm

class RocchioRelevance:

    def __init__(self, matrix):
        self.docVects = matrix.vectorDocs
        from vector_space_model import VectorSpaceModel
        self.model = VectorSpaceModel(matrix)
        self.alpha = 1.0
        self.beta = 0.5
    
    def beginRelevanceRank(self, query, count):
        return self.relevanceRank(query, count)
    
    def relevanceRank(self, query, count):
        
        #use the vector space model implementation to get the top n documents
        results = self.model.getTopNDocumentsForQuery(query, count)
        
        #print out the top 5 words of the top n documents
        for doc in results:
            print(doc[0], end= ": ")
            line = ""
            highestRankingWords = sorted(self.docVects[doc[0]], key=lambda x: x[1], reverse=True)[:5]
            for word in highestRankingWords:
                line += word[0] + ","
            print(line)
            
        print("-" * 15)
        print("Enter the document ids you deem to be most relevant to your query as space seperated values or -1 to end")
        print("e.g: 1 17 213...")
        
        #take a space seperated list of inputs from the user
        inputValues = input()
        splitValues = inputValues.split(" ")
        
        #remove duplicates
        relaventDocuments = set(splitValues)
        
        #end the recurse
        if str(-1) in splitValues:
            return results
        
        #get the vector representation of the current query
        vecDoc = query.vectorDoc
        
        #set the relevance/non-relevance weights
        relevanceWeighting = self.alpha / float(len(relaventDocuments))
        nonRelevanceWeighting = self.beta / (count - len(relaventDocuments))
        
        #create a new document vector for summing up the relavent document values
        from document_vector import DocumentVector
        sumedVect = DocumentVector()
        
        #loop through each relevant document and sum up the vector values
        #NOTE we count every word, even if it's not in the query
        for relevantDocument in relaventDocuments:
            vectorDocForDocument = self.docVects[int(relevantDocument)]
            for word in vectorDocForDocument.values:
                if word in sumedVect.values:
                    sumedVect.values[word] += vectorDocForDocument.values[word]
                else:
                    sumedVect.addValue(word, vectorDocForDocument.values[word])

        #multiply the vector by the relevance weighting
        #add the resulting vector to our query
        for val in sumedVect.values:
            sumedVect.values[val] = sumedVect.values[val] * relevanceWeighting
            vecDoc.values[val] = sumedVect.values[val] if val not in vecDoc.values else (vecDoc.values[val] + sumedVect.values[val])
        
        
        #create a new sumed vector to represent the non-relevent documents
        sumedVect = DocumentVector()
        
        #loop through each non-relevant document and sum up the values
        for nonRelevantDocument in results:
            if str(nonRelevantDocument[0]) not in relaventDocuments:
                vectorDocForDocument = self.docVects[int(nonRelevantDocument[0])] 
                for word in vectorDocForDocument.values:
                    if word in sumedVect.values:
                        sumedVect.values[word] += vectorDocForDocument.values[word]
                    else:
                        sumedVect.addValue(word, vectorDocForDocument.values[word])
                            
        #multiply the vector by the non-relevance weighting
        #substract the non-relevance vector from our query                 
        for val in sumedVect.values:
            sumedVect.values[val] = sumedVect.values[val] *  nonRelevanceWeighting
            vecDoc.values[val] = sumedVect.values[val] if val not in vecDoc.values else (abs(vecDoc.values[val] - sumedVect.values[val]))
            
        #finalize the vector to calculate the magnitude
        vecDoc.finalize()
        
        #set the query to use the newly constructed vector
        query.vectorDoc = vecDoc
        
        #separator to make it slightly more readable 
        print("-" * 15)
        
        #recurse
        return self.relevanceRank(query, count)
                
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            