"""
This program takes the url1 column from 'Hospital_General_Information_url.csv
and searches for all csv/excel files on that page and the "second layer" of
the website after following each link on the page. Downloaded files are stored in `downloaded_files/hospital_name`.
"""

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import os
import urlparse
import time
import sys

# Functions
def make_soup(url):    
    try:
        res = requests.get(url, timeout=5)
        soup = bs(res.text, "html.parser")        
    except Exception:        
        soup = []    
    return(soup)

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
    
    # Create downloaded files folder
    if not os.path.exists("./downloaded_files"):
        os.makedirs("./downloaded_files")

    for index, row in df.iterrows():
    
        # Visit hospital website and make soup
        start_time = time.time()
        hospital_name = row['Hospital Name']
        my_url = row['url1']
        print("----------------------------------")
        print("Scraping Hospital " + str(index) + ": " + hospital_name)
        print("url: " + my_url)
        soup = make_soup(my_url)
    
        # Create hospital specific folder to store downloaded files
        directory = "./downloaded_files/" + hospital_name
        if not os.path.exists(directory):
            os.makedirs(directory)
    
        # Extract all links from front page
        links = []
        if soup:
            for link in soup.find_all('a'):
                current_link = link.get('href')
                current_link = urlparse.urljoin(my_url, current_link)
                links.append(current_link)
        home_links = list(set(links))
    
        # Extract all links from secondary pages
        links = []
        for url in home_links:
            soup = make_soup(url)
            if soup:
                for link in soup.find_all('a'):
                    current_link = link.get('href')
                    current_link = urlparse.urljoin(my_url, current_link)
                    links.append(current_link)
        links = list(set(links))        
        print(str(len(links)) + " webpages found.")
    
        # Extract links to excel, csv and xml files
        files = []
        for link in links:
            link = link.encode('ascii', 'ignore')
            if link.endswith('xlsx') | link.endswith('xls') | link.endswith('csv') | link.endswith('xml'):
                files.append(link)
        print(str(len(files)) + " files found:")
    
        # Save file url's as csv file
        if files:
            file_urls = pd.DataFrame(data={"url": files})
            file_urls.to_csv(directory + "/file_urls.csv", sep=',',index=False)    
    
        # Save Files
        for url in files:
            print(url)
            response = requests.get(url)
            a = urlparse.urlparse(url)
            if a.query:
                fn = a.query
            else:
                fn = url.rsplit('/', 1)[-1]
        
            fn = fn.replace("%20","_")
            fn = fn.replace("dn=","")
            fname = directory + "/" + fn
            with open(fname, 'wb') as f:
                f.write(response.content)
    
        print("Runtime: " + str(time.time() - start_time) + " seconds")

if __name__ == '__main__':
    main()    
