# Round 2 Scraping Code

The initial scraping/crawling process is divided into several rounds. This folder contains the code and output from the second round, which uses the `scrapy` crawling framework.

## File Descriptions
- The `scrapy_price` folder and the `scrapy.cfg` file are the core structures needed for the scrapy framework. Must are created by default, except for the `search_spider.py` file in `./scrapy_price/spiders`, which defines the crawler used for this project.

- `1.get_filelocations.py` calls the spider defined above. It results in a csv file stored in the `file_locations` folder listing the url locations for each hospital. It can be run from the command line in 2 different ways. The first:

    `python 1.get_filelocations.py start_index end_index`

    where `start_index` and `end_index` are integers representing the slice in the `../Hospital_General_Information_url.csv` file to use for searching.
    
    The other approach is to run:
    
    `python 2.scrape_files.py failures.csv`
    
    where `failures.csv` is a file containing a column labeled `failures` with a list of indices of the hospitals to scrape. This file can be automatically created using the `aux_status_check.py` file described below. The output is a hospital-specific csv file containing the locations of potential pricing files.

- `file_locations` contains files corresponding to each hospital in which the url location of the found csv/excel file is stored. There are too many files to upload here, but they can be downloaded from [this dropbox link](https://www.dropbox.com/sh/pe1jd0j3d6b0rbk/AABr0YqZ0iRuOrkl2RPbGLSMa?dl=0).

- `aux_statuscheck.py` runs a bunch of checks and reports a number of statistics based on the files downloaded from the scraping exercise, such as the number of files downloaded etc. It also produces the `failures.csv` containing the indices of the hospitals not yet scraped, which can be used by the `2.scrape_files.py` file as described above.
