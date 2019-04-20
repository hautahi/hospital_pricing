"""
This program searches google using: 'hospital-name'+'city'+ 'keywords'
where 'keywords' include a number of terms related to pricing sheets

It draws from the 'Hospital_General_Information.csv' and returns the
first few google hits, which are then saved to a hospital-specific
csv file in the `urls` folder. These are then searched for
pricing files within the 2.get_locations.py code

We use the google-api-python-client for this. Check out here for what to do to set this up.

https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search
"""

# ------------
# Housekeeping
# ------------

# Load packages
import pandas as pd
import numpy as np
import os.path
import time
from googleapiclient.discovery import build

# Describe keywords (put in quotes)
keywords = ['"chargemaster"','"price list"']

# Data Location
fname = "../Hospital_General_Information.csv"

# Set locations of round 1-3 downloads
round1 = "../round1_scrape/downloaded_files/"
round2 = "./round2_scrape/file_locations/"
round3 = "./urls/"

# Define Google API keys
my_api_key = "AIzaSyBBWLepAgLgsiceVBxyfhTFUKtZ76A17Ts"
my_cse_id = "007191942572901401371:cermqrnt_sq"

# ------------
# Slice dataframe to only include those hospitals that haven't yet had files found
# ------------

start_time = time.time() 
print("Filtering hospitals already scraped ....")

# Read in hospital list
d = pd.read_csv("fname")

# Create columns
d['round1'] = False
d['round2'] = False
d['round3'] = False

# Loop over each hospital
for index, row in d.iterrows():

    # Get name
    name = row['Hospital Name']
    
    # Round 1 Check
    if os.path.exists(round1 + name):
        file_list = os.listdir(round1 + name)
        if file_list:
            row['round1'] = True
            
    # Round 2 Check
    if os.path.exists(round2 + name + ".csv"):
        try:
            df = pd.read_csv(round2 + name + ".csv")
            row['round2'] = True
            
        except:
            pass

    # Round 3 Check
    if os.path.exists(round3 + name + ".csv"):
        try:
            df = pd.read_csv(round3 + name + ".csv")
            row['round3'] = True
            
        except:
            pass
    
    # Add dataframe
    d.iloc[index]  = row

# Label hospitals as having files
d['success'] = d['round1'] | d['round2'] | d['round3']

# Get unsuccessful hospitals
failures = d.index[~d['success']].tolist()

# Slice dataframe
df = d.iloc[failures]

# ------------
# Scrape google search links
# ------------

print("Scraping google search info ....")

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return(res.get('items'))

for _, row in df.iterrows():
    
    results_list = []    
    for kw in keywords:
        
        # Create Search Term
        time.sleep(np.random.uniform(0,2,1))
        search_term = " ".join([row['Hospital Name'],row['City'],str(kw)])
        print(search_term)

        # Conduct Search
        results = google_search(search_term, my_api_key, my_cse_id)
        
        # Gather Results
        if results:
            results_list += [r['link'] for r in results]
    
    if results_list:
        
        # Remove duplicates
        results_list = list(set(results_list))
    
        # Save list of urls to search later
        f = './urls/' + row['Hospital Name'] + '.csv'
        d_results = pd.DataFrame({'urls': results_list})
        d_results.to_csv(f,index=False)

print("--- %s seconds ---" % (time.time() - start_time))
