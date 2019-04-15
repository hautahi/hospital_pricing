"""
This program replaces duplicate hospital names with
unique names by adding the city and state to the name.
"""

import pandas as pd
import collections

# Read in hospital list
d = pd.read_csv("../Hospital_General_Information_url.csv")

# Find duplicates
dups = [item for item, count in collections.Counter(d['Hospital Name'].tolist()).items() if count > 1]

# Loop over each hospital
for index, row in d.iterrows():
    
    # Get name
    name = row['Hospital Name']
    
    # Replace with longer name if a duplicate
    if name in dups:
        
        rep_name = name + " " + row['City'] + " " + row['State']
        
        row['Hospital Name'] = rep_name
        
        d.iloc[index]  = row 

# Overwrite the csv
d.to_csv("../Hospital_General_Information_url.csv",index = False)
