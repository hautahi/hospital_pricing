'''
This program retrieves the files specified in `file_locations`
and stores them in `downloaded_files`.
'''

#-------------------------------------------------------------#
# 1. Setup
#-------------------------------------------------------------#

print("Code is Working...")

import wget
import os
import pandas as pd

#-------------------------------------------------------------#
# 2. Run
#-------------------------------------------------------------#

file_list = os.listdir('file_locations')
file_list = [x for x in file_list if x != '.DS_Store']

for f in file_list:
    
    # Check if folder has already been created
    path = './downloaded_files/' + f.replace(".csv","")
    if not os.path.exists(path):

        try:
            
            # Try to open file if it contains stuff
            d = pd.read_csv('./file_locations/' + f)
            
            # Create Directory
            os.mkdir(path)
            
            # Create list to scrape
            urls = d['file_urls'].tolist()
            
            # Loop over urls and retrieve files
            for i, url in enumerate(urls):
                r = requests.get(url, headers=headers)  

                with open(path + "/" + str(i) + '.' + url.split('.')[-1], 'wb') as p:  
                    p.write(r.content)
            
        except:
            pass
