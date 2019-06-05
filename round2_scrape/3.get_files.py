import os
import pandas as pd
import requests

#-------------------------------------------------------------#
# 2. Find non empty files
#-------------------------------------------------------------#

file_list = os.listdir('file_locations')
file_list = [x for x in file_list if x != '.DS_Store']
print(len(file_list))

non_empty_files = []
for f in file_list:
    
    try:
            
        # Try to open file if it contains stuff
        d = pd.read_csv('./file_locations/' + f)
        
        non_empty_files.append(f)
            
    except:
        pass

print(len(non_empty_files))

#-------------------------------------------------------------#
# 3. Find non empty files
#-------------------------------------------------------------#

headers = {'user-agent': 'test-app/0.0.1'} 
for f in non_empty_files:
    
    path = './downloaded_files/' + f.replace(".csv","")
    files = os.listdir(path)
    
    if len(files) == 0:
        print(f)
        
        # Try to open file if it contains stuff
        d = pd.read_csv('./file_locations/' + f)

        # Create list to scrape
        urls = d['file_urls'].tolist()
        
        try:
            # Loop over urls and retrieve files
            for i, url in enumerate(urls):

                r = requests.get(url, headers=headers)  

                with open(path + "/" + str(i) + '.' + url.split('.')[-1], 'wb') as p:  
                    p.write(r.content)
                    
        except:
            pass     
