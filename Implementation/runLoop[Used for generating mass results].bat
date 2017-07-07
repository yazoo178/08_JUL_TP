
FOR /L %%x IN (1,1,100) DO (
	Python main.py -s stop_list.txt -c documents.txt -i william.txt -o percent_%%x_5_run_results.txt -m p -tf n -idf t
)	