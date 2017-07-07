import argparse
from tf_weighting import Tf_Weighting
from logarithmic_tf_weighting import Logarithmic_Tf_Weighting
from augmented_tf_weighting import Augmented_Tf_Weighting
from boolean_tf_weighting import Boolean_Tf_Weighting
import time, sys, nltk

class EntryPoint:
                
   
    def __init__(self):
        
        #the output file name for the index file
        self.outputName = "index.txt"
        
        #should we step or not
        self.stem = None
        
        #set of stop words
        self.stops = set()
        
        #Should we use an existing index file
        self.useExistingIndexFile = False
        
        #should we use a query id
        self.queryId = -1
        
        #name of output file for results
        self.outputFileName = "results.txt"
        
        #how we calculate the term freq
        #default is n for natural        
        self.tfWeighter = Tf_Weighting()
        
        #how we calculate the inverse
        #doc freq. default is t
        self.idfType = "t"
        
        #how many docs should we return
        #for each query
        #default is 10
        self.numberOfDocs = 10
        
        #if we are using rocchio relevance mode
        #then set a value
        self.rrAmount = - 1
        
        #Should we execute on the fly
        self.onTheFly = 0
    
	#runs the ir system
    def runIRS(self, path):
        
        from information_retrieval_system import InformationRetrievalSystem

        system = InformationRetrievalSystem(self.outputName, self.stem,
                                            self.stops, self.useExistingIndexFile,
                                            self.queryId, self.outputFileName,
                                            self.tfWeighter, self.idfType,
                                            self.numberOfDocs, self.rrAmount,
                                            self.onTheFly)
                                            
        system.Run(path)
                   
            
    #updates/creates a file for how long the system took to run the output
    def printOutputTiming(self, startTime, args):
        end = time.time()
        timingFile = open("timings.txt", 'a')
        settings = str(sys.argv)
        timingFile.write(settings + ":" + str(end - startTime) + '\n')
    
    #runs a boolean model
    def runBooleanModel(self):
        from boolean_query_model import BooleanQueryModel
        queryModel = BooleanQueryModel(self.matrix)
        resultIds = queryModel.query("roots", self.stem)
        print(resultIds)
        

    def main(self):
        #create input parser
        parser = argparse.ArgumentParser()
            
        #add non mandatory argument for stoplist file
        parser.add_argument('-s', action='store', dest='stop_list_path',help='use stoplist file')
    
        #add mandatory argument for collections file
        parser.add_argument('-c', action='store',help='the file path to the documents', dest='collection', required=True)
    
        #add mandatory argument for index (output) file
        parser.add_argument('-i', action='store',help='the index file', dest='index', required=True)
        
         #add non mandatory argument for if we should use the existing index file
        parser.add_argument('-I', action='store_true',help='use existing index file', dest='use_index')
        
        #add non mandatory argument for if we should compute on the fly
        parser.add_argument('-F', action='store_true',help='use on the fly computation', dest='use_fly')
    
        #add non mandatory argument of whether or not to use stemming
        parser.add_argument('-m', action='store',help='specify type of stemmer', dest='stem')
        
        #add non mandatory argument of whether or not to use stemming
        parser.add_argument('-q', action='store',help='use query id', dest='query_id', type=int)
        
        #add non mandatory argument for collections file
        parser.add_argument('-o', action='store',help='output file name', dest='output_file')
        
        #add non mandatory argument for term freq type
        parser.add_argument('-tf', action='store',help='term frequency calculation type', dest='tf_type')
        
        #add non mandatory argument for the inverse document freq type
        parser.add_argument('-idf', action='store',help='inverse doc frequency calculation type', dest='idf_type')
        
        #add non mandatory arugment for top N results. I.E number of results returned by query
        parser.add_argument('-n', action='store',help='the number of documents to return for query', dest='numberOfDocs')
        
        #add non mandatory arugment to use rocchio relevance
        parser.add_argument('-r', action='store',help='rocchio relevance mode', type=int, nargs='?', const=10, dest='rr')
    
        #get arugments
        args = parser.parse_args()
    
        #if we supplied a stop list then load the data
        if args.stop_list_path:
            from StopListLoader import loadStopList
            data = loadStopList(args.stop_list_path)
            self.stops.update(data)
         
        #if we supplied a name for the output file then set it
        if args.index: 
            self.outputName = args.index
                
         #if we activated the stemming flag
		 #we have the option to supply different types of stemmers 
		 #aswell as a lemmatizer 
        if args.stem:
            stemmer = None
            if args.stem == "p":
                from nltk.stem import PorterStemmer
                stemmer = PorterStemmer()  
                self.stem = lambda x: stemmer.stem(x)    
            elif args.stem == "s":
                from nltk.stem.snowball import SnowballStemmer
                stemmer = SnowballStemmer("english")
                self.stem = lambda x: stemmer.stem(x)    
            elif args.stem == "l":
                from nltk.stem.lancaster import LancasterStemmer
                stemmer = LancasterStemmer()
                self.stem = lambda x: stemmer.stem(x)    
            elif args.stem == "lem":
                nltk.download("wordnet")
                from nltk.stem import WordNetLemmatizer  
                stemmer = WordNetLemmatizer()
                self.stem = lambda x:stemmer.lemmatize(x)
            
        #if -I is set then then set useExistingIndexFile to true
        if args.use_index:
            self.useExistingIndexFile = True
            
        #If we wish to get the result set for just a single query
        if args.query_id:
            self.queryId = int(args.query_id)
        
        #the name of the results file when output
        if args.output_file:
            self.outputFileName = args.output_file
            
        #the number of documents we should return for a query
        #set to -1 for optimized result set
        if args.numberOfDocs:
            self.numberOfDocs = int(args.numberOfDocs)
        
        #the type of term freq to use
        if args.tf_type:
            if args.tf_type == "n":
                self.tfWeighter = Tf_Weighting()
            elif args.tf_type == "l":
                self.tfWeighter = Logarithmic_Tf_Weighting()
            elif args.tf_type == "a":
                self.tfWeighter = Augmented_Tf_Weighting()
            elif args.tf_type == "b":
                self.tfWeighter = Boolean_Tf_Weighting()
                
        #the type of inverse doc freq to use
        if args.idf_type:
            if args.idf_type == "p":
                self.idfType = "p"
                
        #sets how many documents should be displayed
        #when using rocchio relevance
        if args.rr:
            self.rrAmount = int(args.rr)
        
		#You can only use relevance feedback mode when a query id is specified
        if self.queryId == -1 and self.rrAmount != -1:
            sys.exit("If you are using rocchio relevance you must supply a query id[-q id]")

        if args.use_fly:
            self.onTheFly = 1
        
		#you cannot use on the fly generation with relevance feedback
        if self.onTheFly == 1 and self.rrAmount != -1:
            sys.exit("If you are using rocchio relevance you cannot use on the fly generation")
        
        #run the IR system
        start = time.time()
        self.runIRS(args.collection)
        self.printOutputTiming(start, args)
    
#entry point
entry = EntryPoint()
entry.main()