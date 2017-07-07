The implementation can be found in the /Implementation folder
The report can be found in the same folder as this file - 'results.pdf'

The data I used to generate the results can be found in the /results folder



To run the solution, navigate into the Implemetation folder and run:

Python main.py

options:

-h prints help message and exits program
-s use the stoplist file[OPTIONAL]
-c the collection file
-i the index file [this will output a new index file with the given name]
-I use an existing index file[OPTIONAL][Name of index file is taken from -i param][The index file must be in the same directory]
-m use stemming [OPTIONAL][OPTIONS: p, s, l, lem][porter, snowball, lancaster, wordnetlemmatizer respectively]
-q a query id [OPTIONAL][Used to execute a single query]
-o output name for results file
-tf the flavour of tf [OPTIONAL][Default is n(natural)][OPTIONS: b, l, a][boolean, logarithmic, augmented respectively]
-idf the flavour of idf [OPTIONAL][Default is t][OPTIONS: p][prob idf]
-n number of documents to return. Higher n == higher recall but lower precision.[Default is 10][set to -1 to get more accurate optimized result set]
-r use relevance feedback mode[OPTIONAL][OPTIONS: n][a numerical value of how many documents you will have to mark as relevant. default is 10]
-F generate output on the fly [OPTIONAL] In order to implement the relevance feedback, I had to store the tf.idf vectors for later modifaction. This flag will stop the system from storing the tf-idf values (cannot be used with rr mode)


IF YOU STORE A STEMMED INDEX FILE AND THEN WISH TO RUN A NON-STEMMED CONFIG REMEMBER TO GENERATE A NON-STEMMED INDEX FILE!

examples:

#prints help then exits
Python main.py -h

#run with stop list, create a new index file called william.txt output the results in a file called run_results.txt, use stemming(porter), use the natural tf.idf weightings, generate on the fly
Python main.py -s stop_list.txt -c documents.txt -i william.txt -o run_results.txt -m p -F

#run with stop list, create a new index file called william.txt, output the results in a file called run_results.txt, use stemming(porter) and use a tf type of boolean (default idf)
Python main.py -s stop_list.txt -c documents.txt -i william.txt -o run_results.txt -m p -tf b

#same as above, but this time use a previously created index file called william.txt and return the top 20 documents.
Python main.py -s stop_list.txt -c documents.txt -i william.txt -o run_results.txt -m p -tf b -I -n 20

#run without stoplist and stemming, output results in a file called run_results.txt and use a tf type of augmented
Python main.py -c documents.txt -i william.txt -o run_results.txt -tf a

#run with stop list, create a new index file called william.txt, output the results in a file called run_results.txt, use stemming(porter), use a tf type of boolean and use an idf type of p
Python main.py -s stop_list.txt -c documents.txt -i william.txt -o run_results.txt -m p -tf b -idf p

#runs in relevance feedback mode. Use a stop list and natural tf.idf weighting. Run against query 30 with top 5 documents displayed
Python main.py -s stop_list.txt -c documents.txt -i william.txt -o f_run_results.txt -tf n -idf t -r 5 -q 30

#runs with a stop list, creates an index file called william.txt, uses a porter stemmer, natural tf.idf, generates on-the-fly and produces an optimum output result file (0.26 f-measure)
#this produces our best output file
Python main.py -s stop_list.txt -c documents.txt -i william.txt -o 7_run_results.txt -m p -tf n -idf t -F -n -1