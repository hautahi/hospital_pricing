"""
This program summarizes the file counts from each of the scraping round.
There are 2 methods. One based on hospita names. Another just based on files in the folders.
There's a slight diffence. Not sure why.
"""

# -------------------
# Housekeeping
# -------------------

import pandas as pd
import os

# Set locations of round 1-3 downloads
round1 = "../round1_scrape/downloaded_files/"
round2 = "../round2_scrape/file_locations/"
round3 = "../round3_scrape/file_locations/"

# -------------------
# Second way of doing it
# -------------------

# Read hospital list
d = pd.read_csv("../Hospital_General_Information_url.csv")
d = d[['Hospital Name']]

# Create columns
d['round1'] = False
d['round2'] = False
d['round3'] = False
d['round1_count'] = 0
d['round2_count'] = 0
d['round3_count'] = 0

# Loop over each hospital
for index, row in d.iterrows():

    # Get name
    name = row['Hospital Name']
    
    # Round 1 Check
    if os.path.exists(round1 + name):
        file_list = os.listdir(round1 + name)
        if file_list:
            row['round1'] = True
            row['round1_count'] = len(file_list) - 1
            
    # Round 2 Check
    if os.path.exists(round2 + name + ".csv"):
        try:
            df = pd.read_csv(round2 + name + ".csv")
            row['round2'] = True
            row['round2_count'] = df.shape[0]
            
        except:
            pass

    # Round 3 Check
    if os.path.exists(round3 + name + ".csv"):
        try:
            df = pd.read_csv(round3 + name + ".csv")
            row['round3'] = True
            row['round3_count'] = df.shape[0]
            
        except:
            pass
    
    # Add dataframe
    d.iloc[index]  = row 

# Print results
print("Round 1 Scraped " + str(d['round1'].sum()) + " hospitals")
print("Round 2 Scraped " + str(d['round2'].sum()) + " hospitals")
print("Round 3 Scraped " + str(d['round3'].sum()) + " hospitals")

print("Round 1 Scraped " + str(d['round1_count'].sum()) + " files")
print("Round 2 Scraped " + str(d['round2_count'].sum()) + " files")
print("Round 3 Scraped " + str(d['round3_count'].sum()) + " files")

# -------------------
# Second way of doing it
# -------------------

# Round 1 Check
file_list1 = os.listdir(round1)
file_list1 = [x for x in file_list1 if not x.startswith(".")]
nonempty1 = 0
for f in file_list1:
    file_list = os.listdir(round1 + f)
    if file_list:
        nonempty1 += 1
        
# Round 2 Check
file_list = os.listdir(round2)
nonempty2 = 0
for f in file_list:
    try:
        df = pd.read_csv(round2 + f)
        nonempty2 += 1

    except:
        pass

# Round 3 Check
file_list = os.listdir(round3)
nonempty3 = 0
for f in file_list:
    try:
        df = pd.read_csv(round3 + f)
        nonempty3 += 1

    except:
        pass    

# Print results
print("Round 1 Scraped " + str(nonempty1) + " hospitals")
print("Round 2 Scraped " + str(nonempty2) + " hospitals")
print("Round 3 Scraped " + str(nonempty3) + " hospitals")
