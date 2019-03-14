import urllib3
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import os
import urlparse
from urlparse import urljoin
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

    # First element of args is the function name
    args = sys.argv[1:]

    # Check to make sure the proper numbr of arguments exist
    if not args or len(args) < 2:
        print('usage: start_index end_index')
        sys.exit(1)

    # Assign parameters
    s1, s2 = [int(x) for x in args]

    # Read url's
    df = pd.read_csv("Hospital_General_Information_url.csv")

    # Restrict
    d = df[s1:s2]

    # Create downloaded files folder
    if not os.path.exists("./downloaded_files"):
        os.makedirs("./downloaded_files")

    for index, row in d.iterrows():
    
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
                current_link = urljoin(my_url, current_link)
                links.append(current_link)
        home_links = list(set(links))
    
        # Extract all links from secondary pages
        links = []
        for url in home_links:
            soup = make_soup(url)
            if soup:
                for link in soup.find_all('a'):
                    current_link = link.get('href')
                    current_link = urljoin(my_url, current_link)
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
