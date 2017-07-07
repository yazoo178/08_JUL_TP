def loadStopList(file):
    stops = set()
    fileData = open(file,'r')
     
    for line in fileData:
        stops.add(line.strip())
    return stops
