Python main.py -s stop_list.txt -c documents.txt -i william.txt -o 1_run_results.txt -m p -tf l -idf p -n -1 -r 10 -q 53
Python main.py -s stop_list.txt -c documents.txt -i william.txt -o 2_run_results.txt -m p -tf n -idf p -F -n -1
Python main.py -s stop_list.txt -c documents.txt -i william.txt -o 3_run_results.txt -m p -tf a -idf p -F
Python main.py -s stop_list.txt -c documents.txt -i william.txt -o 4_run_results.txt -m p -tf b -idf p -F

Python main.py -s stop_list.txt -c documents.txt -i william.txt -o 5_run_results.txt -m p -tf n -idf t -F
Python main.py -s stop_list.txt -c documents.txt -i william.txt -o 6_run_results.txt -m p -tf l -idf t -F
Python main.py -s stop_list.txt -c documents.txt -i william.txt -o 7_run_results.txt -m p -tf a -idf t -F
Python main.py -s stop_list.txt -c documents.txt -i william.txt -o 8_run_results.txt -m p -tf b -idf t -F

Python main.py -c documents.txt -i william.txt -o 9_run_results.txt -m p -tf n -idf t -F

Python main.py -s stop_list.txt -c documents.txt -i william.txt -o 10_run_results.txt -F
