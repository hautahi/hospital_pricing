"""

"""

import pandas as pd
import os
import collections

# Set locations of round 1-3 downloads
round1 = "../round1_scrape/downloaded_files/"
round2 = "./file_locations/"

# Read in hospital list
d = pd.read_csv("../Hospital_General_Information_url.csv")

# Get relevant columns
d = d[['Hospital Name', 'url1']]

# Create columns
d['excel_count'] = ""
d['round1'] = False
d['round2'] = False
d['round2_attempt'] = False

# Loop over each hospital
for index, row in d.iterrows():

    # Get name
    name = row['Hospital Name']

    # Round 1 check if files have been downloaded
    if os.path.exists(round1 + name):

        # Count files
        file_list = os.listdir(round1 + name)
        row['excel_count'] = len([i for i in file_list if (i.endswith("xlsx")) | (i.endswith("xls")) | i.endswith(".csv")])
        
        row['round1'] = row['excel_count'] > 0
        
    # Round 2 check if hospital has been processed/file has been found
    if os.path.exists(round2 + name + ".csv"):
        
        row['round2_attempt'] = True
        
        try:
            df = pd.read_csv(round2 + name + ".csv")
            row['round2'] = True
            
        except:
            pass
    
    # Add dataframe
    d.iloc[index]  = row 
    
# Label hospitals as having files
d['success'] = d['round1'] | d['round2_attempt']

# Get unsuccessful hospitals
failures = d.index[~d['success']].tolist()

# Save those hospitals
df = pd.DataFrame({'failures': failures})
df.to_csv("failures.csv",index=False)
