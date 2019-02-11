"""
sudo yum install pip git tmux

curl -O https://bootstrap.pypa.io/get-pip.py
python get-pip.py --user

pip install numpy pandas --user

https://github.com/abenassi/Google-Search-API
pip install git+https://github.com/abenassi/Google-Search-API
"""

# Load packages
import pandas as pd
import numpy as np
from google import google
import os.path
import time

start_time = time.time() 

# Load Data
original = "Hospital_General_Information.csv"
new = "Hospital_General_Information_url.csv"
if os.path.isfile(new):
    d = pd.read_csv(new)
else:
    d = pd.read_csv(original)
    d['url1'] = ""
    d['url2'] = ""
    d['url3'] = ""

for index, row in d.iterrows():
    if ((row["url1"] == "") | (str(row["url1"])=='nan')) & (index > 0):
        
        # Create Search Term
        time.sleep( np.random.uniform(0,2,1) )
        print(index)
        search_term = " ".join([row['Hospital Name'],row['City'],row['State'],str(row['ZIP Code'])])
        print(search_term)
        
        # Conduct Search
        results, i = [], 0
        while (not results) & (i < 20):          
            i += 1
            results = google.search(search_term, 1)
        # Add url's
        if (i == 20) | (len(results)<3):
            row["url1"] = ""
            row["url2"] = ""
            row["url3"] = ""
        else:
            row["url1"] = str(results[0].link)
            row["url2"] = str(results[1].link)
            row["url3"] = str(results[2].link)
        print(row['url1'])
        # Add dataframe
        d.iloc[index]  = row

        # Print dataframe
        d.to_csv(new,index=False)

print("--- %s seconds ---" % (time.time() - start_time))
