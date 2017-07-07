import re
import pylab as p
import numpy as np
import matplotlib.pyplot as plt
import re

file = open("cacm_gold_std.txt")
goldDocs = {}

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump
    
for line in file:
    line = re.search("(\d+) (\d+)", line)
    if line:
        queryId = int(line.group(1))
        docId = int(line.group(2))
    
        if queryId in goldDocs:
            goldDocs[queryId].append(int(docId))
        else:
            goldDocs[queryId] = []
            goldDocs[queryId].append(int(docId))
            
    
results = []
            
for i in range(500, 5000, 10):
   fileResults = open("nPer/" + "percent_" + str(i) + "_" + "5" + "_" + "run_results.txt")
   fileDocs = {}        
   for line in fileResults:
      line = re.search("(\d+) (\d+)", line) 
      if line:
          queryId = int(line.group(1))
          docId = line.group(2)
          
          if queryId in fileDocs:
              fileDocs[queryId].append(int(docId))
          else:
              fileDocs[queryId] = []
              fileDocs[queryId].append(int(docId))  
           
   results.append(fileDocs)
   

   
   
recallRates = []
presRates = []

for index,outputFile in enumerate(results):
   recall = []
   pres = []
   for goldDoc in goldDocs:
       inCount = 0
       for line in outputFile:
           for element in outputFile[line]:
              if element in goldDocs[goldDoc] and goldDoc == line:
                  inCount+=1
       recall.append(inCount / len(goldDocs[goldDoc]))
       pres.append(inCount/ len(outputFile[line]))
   recallRates.append(recall)
   presRates.append(pres)
   
   
averageRecalls = []
for item in recallRates:
    total = 0
    for rate in item:
        total +=rate
    averageRecalls.append((total / len(item)))



averagePres = []
for item in presRates:
    total = 0
    for rate in item:
        total +=rate
    averagePres.append((total / len(item)))
    

averageFMeasures = []
for pres, recall in zip(presRates, recallRates):
    totalPres = 0
    for ratePres in pres:
        totalPres += ratePres
    
    totalRecall = 0
    for rateRecall in recall:
        totalRecall += rateRecall
      
        
    totalPres = totalPres / len(pres)  
    totalRecall = totalRecall / len(recall)
    averageFMeasures.append((2 * (totalPres * totalRecall)) / (totalPres + totalRecall))





plt.show()

X = [x/100 for x in range(500, 5000, 10)]
#Y = averageRecalls
#Y2 = averagePres
#p.plot(X,Y, label = "Average Recall")
#p.plot(X,Y2, label = "Average Precision")
p.plot(X, averageFMeasures, label= "Harmonic Mean")
p.xlabel("Permitted % difference between vector simularity rates", fontsize=13)
p.ylabel('Rate (0-1)', fontsize=13)
p.legend( loc='lower right')
p.suptitle("The F-Measure rate for increasing the percentage before cut off (-s-m-tf:n-idf:t)", fontsize=14)

p.show()













