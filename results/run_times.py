import numpy as np
import matplotlib.pyplot as plt
import re

file = open("timings.txt", "r")
lables = ['-s-m-tf:l-idf:p', '-s-m-tf:n-idf:p', '-s-m-tf:a-idf:p','-s-m-tf:b-idf:p',
          '-s-m-tf:n-idf:t', '-s-m-tf:l-idf:t','-s-m-tf:a-idf:t', '-s-m-tf:b-idf:t', '-m-tf:n-idf:t', '-s-tf:n-idf:t']

values = []
for line in file.readlines():
    match = re.search("\d+.\d+", line)
    values.append(float(match.group()))
    



count = len(values)

ind = np.arange(count)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, values, width, color='b')


# add some text for labels, title and axes ticks
ax.set_ylabel('Seconds')
ax.set_title('Time taken to execute IR system with different parameters')
ax.set_xticks(ind + width)
ax.set_xticklabels(lables)




#def placeLabel(rects):
    # attach some text labels
#    for rect in rects:
 #       height = rect.get_height()
 #       ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
  #              '%d' % int(height),
   #             ha='center', va='bottom')

#placeLabel(rects1)

plt.show()