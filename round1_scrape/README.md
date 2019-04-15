# Round 1 Scraping Code

The initial scraping/crawling process is divided into several rounds. This folder contains the code and output from the first round.

## File Descriptions
- `1.google_search.py` takes the hospital list `../Hospital_General_Information.csv` and grabs the top 3 pages in a google search, which are then stored as additional columns in `../Hospital_General_Information_url.csv`.

- `2.scrape_files.py` scrapes all `.csv`, `.xml`, `.xls`, and `.xlsx` files from the webpage defined by the first url stored in `Hospital_General_Information_url.csv` and the webpages of all links on that first page (2-layer search). It can be run from the command line in 2 different ways. The first:

    `python 2.scrape_files.py start_index end_index`

    where `start_index` and `end_index` are integers representing the slice in the csv file to use for searching.
    
    The other approach is to run:
    
    `python 2.scrape_files.py failures.csv`
    
    where `failures.csv` is a file containing a column labeled `failures` with a list of indices of the hospitals to scrape. This file can be automatically created using the `aux_status_check.py` file described below. The output is a hospital-specific folder in the `downloaded_files` folder containing all the files found as well as a `file_url.csv` file containing the url of each scraped file.

- `downloaded_files` contains folders corresponding to each hospital in which the scraped files from that hospital is stored. There are too many files to upload here, but they can be downloaded from [this dropbox link](https://www.dropbox.com/sh/ksmp1am98y8sc6t/AAA0APzPZGWx8XfAmW0Kjcw3a?dl=0).

There are also a number of "auxiliary" files that perform some ad-hoc tasks.

- `aux_replacedups.py` replaces duplicate hospital names in `../Hospital_General_Information_url.csv` with unique names by adding the city and state to the name. This is best done before running `2.scrape_files.py`.

- `aux_statuscheck.py` runs a bunch of checks and reports a number of statistics based on the files downloaded from the scraping exercise, such as the number of files downloaded etc. It also produces the `failures.csv` containing the indices of the hospitals not yet scraped, which can be used by the `2.scrape_files.py` file as described above.
