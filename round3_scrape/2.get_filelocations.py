'''
This program calls the spider defined in `./scrapy_price/spiders/search_spider.py`
to scrape the url location of csv/excel files 1 layer deep of the websites defined
in the hospital-specific csv files in the `urls` folder.
It saves the location into a hospital-specific csv file in `file_locations`.
'''

#-------------------------------------------------------------#
# 1. Setup
#-------------------------------------------------------------#

# Load packages
import pandas as pd
import os
import subprocess
from urllib.parse import urlparse
import time

# Set locations of input/output folders
file_list = os.listdir("./urls")
done_files = os.listdir("./file_locations")

#-------------------------------------------------------------#
# 2. Define Function
#-------------------------------------------------------------#

# Read hospital list
d_hosp = pd.read_csv("../Hospital_General_Information_url.csv")

# Get list of hospitals that have not yet been scraped
files = list(set(file_list) - set(done_files))

start_time1 = time.time()
for f in files:
        
    print("----------------------------------")
    print("Processing Hospital " + f)
    print(time.ctime(time.time()))
        
    start_time = time.time()

    # Get original scraped url's from round 1 and add to allowed domains 
    name = f.replace(".csv","")
    df = d_hosp[d_hosp['Hospital Name'] == name]
    urls_original = df['url1'].tolist() + df['url2'].tolist() + df['url3'].tolist()
    allowed_doms = list(set([urlparse(u).netloc for u in urls_original]))
    
    # Get new url's from google search in this round
    d = pd.read_csv("./urls/" + f)
    urls = d['urls'].tolist()
    
    # Filter according to presence of hospital name or original domains
    # (This removes a lot of linkedin/facebook links that google search returned)
    a = name.split() + allowed_doms
    a = [x.lower() for x in a]
    url_list = []
    for u in urls:    
        if any(x in u.lower() for x in a):
            url_list.append(u)
    
    # Add the filtered urls to allowed domains
    allowed_doms += [urlparse(u).netloc for u in url_list]
    
    # If there are any url's remaining, the search them
    if url_list:
        
        # Save the list of url's to a temp file
        df = pd.DataFrame({'urls': url_list})
        df.to_csv("temp_urls.csv",index=False)
        
        # Save the list of allowed domains to a temp file
        df = pd.DataFrame({'doms':allowed_doms})
        df.to_csv("temp_doms.csv",index=False)
        
        # Specify to scrapy where results should be stored
        # csv file is specified in custom settings using the -s flag in terminal call 
        file_arg = "FEED_URI=file_locations/" + f
        
        # Call scrapy crawler and suppress the output
        FNULL = open(os.devnull,'w')
        retcode = subprocess.call(["scrapy", "crawl", "file_search", "-s", file_arg],stdout=FNULL,stderr=subprocess.STDOUT)

    else:
        print("no url")

print("---Total Job: %s seconds ---" % (time.time() - start_time1))

