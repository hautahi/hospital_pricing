import pandas as pd
import os
import collections

def list2range(lst):
    '''make iterator of ranges of contiguous numbers from a list of integers'''

    tmplst = lst[:]
    tmplst.sort()
    start = tmplst[0]

    currentrange = [start, start + 1]

    for item in tmplst[1:]:
        if currentrange[1] == item:
            # contiguous
            currentrange[1] += 1
        else:
            # new range start
            yield tuple(currentrange)
            currentrange = [item, item + 1]

    # last range
    yield tuple(currentrange)

# -----------------------
# Count up a bunch of stuff about the existing scraped files
# -----------------------

print("Counting stuff from hospital files ...")

# Read in hospital list
d = pd.read_csv("Hospital_General_Information_url.csv")

# Create columns
d['checked'] = ""
d['url_doc'] = ""
d['csv_count'] = ""
d['excel_count'] = ""
d['xml_count'] = ""

# Loop over each hospital
for index, row in d.iterrows():
    
    # Get name
    name = row['Hospital Name']
    
    # Check if folder has been created
    if os.path.exists("./downloaded_files/" + name):
        
        row['checked'] = 1
        
        # Count files
        file_list = os.listdir("./downloaded_files/" + name)
        row['excel_count'] = len([i for i in file_list if (i.endswith("xlsx")) | (i.endswith("xls"))])
        row['xml_count'] = len([i for i in file_list if i.endswith(".xml")])
        csv_count = len([i for i in file_list if i.endswith(".csv")])
         
        # Check if the csv file documenting the file locations has been created
        if os.path.isfile("./downloaded_files/" + name + "/file_urls.csv"):
            row['url_doc'] = 1
            row['csv_count'] = csv_count - 1
        else:
            row['csv_count'] = csv_count
    
        # Add dataframe
        d.iloc[index]  = row  

# -----------------------
# Count the file types
# -----------------------

# Reformat
d['csv_count'] = pd.to_numeric(d['csv_count']) 
d['excel_count'] = pd.to_numeric(d['excel_count']) 
d['xml_count'] = pd.to_numeric(d['xml_count']) 

# Define count variables
d['number_files'] = d['csv_count'] + d['excel_count'] + d['xml_count']
d['any_files'] = d['number_files'] > 0
d['any_excel'] = (d['csv_count'] > 0) | (d['excel_count'] > 0)
d['any_xml'] = d['xml_count'] > 0

print("Number of Hospitals where any files were found:")
print(d['any_files'].sum())

print("Number of hospitals with an excel file:")
print(d['any_excel'].sum())

print("Number of hospitals with an xml file:")
print(d['any_xml'].sum())

print("Total number of excel files downloaded:")
print(d['csv_count'].sum() + d['excel_count'].sum())

print("Total number of xml files downloaded:")
print(d['xml_count'].sum())

# -----------------------
# Record the hospitals with missing data
# -----------------------

not_checked, no_doc = [], []
for index, row in d.iterrows():
    
    if row['checked'] != 1:
        not_checked.append(index)
        
    if row['url_doc'] != 1:
        no_doc.append(index)

print("Total number of hospitals scraped:")
print(d.shape[0]-len(not_checked))

print("Total number of hospitals without the url's listed:")
print(len(no_doc))

print("Total number of hospitals not yet scraped:")
print(len(not_checked))

print("Identifiers of hospitals not yet been scraped:")
print([i for i in list2range(not_checked)])

# -------------------
# Check url's for duplicates
# -------------------

url = d['url1']
dups = [item for item, count in collections.Counter(url).items() if count > 1]

print("Only " +str(len(set(url))) + " of " +str(len(url)) + " url's were unique.")

print("Here are the duplicates:")
print(dups)
