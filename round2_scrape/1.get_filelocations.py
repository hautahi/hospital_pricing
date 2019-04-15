'''
This program calls the spider defined in `./scrapy_price/spiders/search_spider.py`
to scrape the url location of csv/excel files 3 layers deep into hospital websites.
It saves the location into a hospital-specific csv file.
'''

#-------------------------------------------------------------#
# 1. Setup
#-------------------------------------------------------------#

print("Code is Working...")

import subprocess
import os
import pandas as pd
from urllib.parse import urlparse
import sys
import time

#-------------------------------------------------------------#
# 2. Define Function
#-------------------------------------------------------------#

def main():
    
    # Read the input file with hospital info and restrict to relevant rows
    print('Reading the main input file...\n')
    d_name = "../Hospital_General_Information_url.csv"
    d = pd.read_csv(d_name)
    
    # First element of args is the function name
    args = sys.argv[1:]

    # Assign parameters either based on command line input or a filename
    # Slice dataframe according to either list or provided integers
    if len(args) == 2:
        s1, s2 = [int(x) for x in args]
        df = d[s1:s2]
    else:
        fail = pd.read_csv(args[0])
        fail = fail['failures'].tolist()
        df = d.iloc[fail]

    # Define user agent
    #h = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"}

    # Loop over hospitals
    start_time1 = time.time()
    for index, row in df.iterrows():

        hospital_name = row['Hospital Name']
        my_url = row['url1']
        
        print("----------------------------------")
        print("Processing Hospital " + str(index) + ": " + hospital_name)
        print("url: " + my_url)
        print(time.ctime(time.time()))
        
        start_time = time.time()
                            
        # Start search at this url (sets the start_urls parameter in the spider)
        url_arg = "url=" + my_url
        
        # Restrict searches to this domain (sets the allowed_domains parameter in the spider)
        allowed_domain_arg = "all_dom=" + urlparse(my_url).netloc

        # Record results in this csv file (adjusts custom settings using the -s flag) 
        file_arg = "FEED_URI=file_locations/" + hospital_name + ".csv"

        # Hospital key word
        hosp = "hospital=" + hospital_name.replace(" ", "_")

        # Call scrapy crawler and suppress the output
        FNULL = open(os.devnull,'w')
        retcode = subprocess.call(["scrapy", "crawl", "file_search", "-s", file_arg,"-a",allowed_domain_arg,"-a",url_arg, "-a", hosp],stdout=FNULL,stderr=subprocess.STDOUT)
        
        # Print duration and update loop variables
        print("--- %s seconds ---" % (time.time() - start_time))

    print("---Total Job: %s seconds ---" % (time.time() - start_time1))

if __name__ == '__main__':
    main()
