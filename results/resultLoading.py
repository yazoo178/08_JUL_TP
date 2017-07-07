import re
import pylab as p
import numpy as np
import matplotlib.pyplot as plt
import re

file = open("cacm_gold_std.txt")
lables = ['-s-m-tf:l-idf:p', '-s-m-tf:n-idf:p', '-s-m-tf:a-idf:p','-s-m-tf:b-idf:p',
          '-s-m-tf:n-idf:t', '-s-m-tf:l-idf:t','-s-m-tf:a-idf:t', '-s-m-tf:b-idf:t', '-m-tf:n-idf:t', '-s-tf:n-idf:t']

goldDocs = {}

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
            
for i in range(1, 11):
   fileResults = open(str(i) + "_" + "run_results.txt")
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


   
averageFMeasures = {}
for pres, recall, key in zip(presRates, recallRates, lables):
    totalPres = 0
    for ratePres in pres:
        totalPres += ratePres
    
    totalRecall = 0
    for rateRecall in recall:
        totalRecall += rateRecall
      
        
    totalPres = totalPres / len(pres)  
    totalRecall = totalRecall / len(recall)
    print(totalPres)
    print(totalRecall)
    averageFMeasures[key] = (2 * (totalPres * totalRecall)) / (totalPres + totalRecall)
    
    

orderedF = sorted(averageFMeasures.items(), key = lambda x:x[1], reverse=True)
 
outputRecallRates = open("recall_rates.txt", "w")
averageRecalls = {}
for item, key in zip(recallRates,lables) :
    total = 0
    for rate in item:
        outputRecallRates.write(str(rate) + "\t")
        total +=rate
    averageRecalls[key] = (total / len(item))
    outputRecallRates.write("\n")
ordered = sorted(averageRecalls.items(), key = lambda x:x[1], reverse=True)

   
averagePres = {}

for item, key in zip(presRates,lables) :
    total = 0
    for rate in item:
        total +=rate
    averagePres[key] = (total / len(item))
    
orderedPres = sorted(averagePres.items(), key = lambda x:x[1], reverse=True)
 


outputRecall = open("average_recalls.txt", "w")

for item in ordered:
    outputRecall.write(str(item[0]) + " " + str(item[1]))
    outputRecall.write("\n")
    
    
outputPres = open("average_presisions.txt", "w")

for item in orderedPres:
    outputPres.write(str(item[0]) + " " + str(item[1]))
    outputPres.write("\n")
    
    
outputAv = open("average_fmeasure.txt", "w")

for item in orderedF:
    outputAv.write(str(item[0]) + " " + str(item[1]))
    outputAv.write("\n")    
    
    
    
    
    
    
    
    
presRatesNew = [0.22, 0.23, 0.21, 0.18, 0.24, 0.23, 0.22, 0.19, 0.23, 0.20]
presRatesNew = sorted(presRatesNew, reverse=True)
    
count = len(presRatesNew)


ind = np.arange(count)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, presRatesNew, width, color='r')
#rects2 = ax.bar(ind + 0.35, [i[1] for i in orderedPres], width, color='b')
# add some text for labels, title and axes ticks
ax.set_ylabel('Rate of each tf.idf output type')
ax.set_xlabel('tf.idf output types')
ax.set_title('Average F-Measure rate')
ax.set_xticks(ind + width)
ax.set_xticklabels(i[0] for i in ordered)


plt.show()    
    
  
    
    
    
    
    
    
    
    
    
    
    
    
    
