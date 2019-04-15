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

## AWS Setup Instructions
1. Setup instance on the AWS website
2. Login to AWS instance via: `ssh -i amazonkey.pem ec2-user@instance-address.amazonaws.com`
3. Setup AWS instance with: `sudo yum install python git tmux pip`.
4. The above setup sometimes messes up `pip`. If this is the case run `curl -O https://bootstrap.pypa.io/get-pip.py` and `python get-pip.py --user`.
5. Run `sudo pip install numpy pandas`
6. Install the [google search api](https://github.com/abenassi/Google-Search-API) package with `pip install git+https://github.com/abenassi/Google-Search-API`
7. Transfer file to instance: `scp -i amazonkey.pem file_name ec2-user@instance-address.amazonaws.com:`
8. Transfer folder to instance: `scp -i amazonkey.pem -r folder_name ec2-user@instance-address.amazonaws.com:`
9. Transfer files back to local machine: `scp -i amazonkey.pem -r ec2-user@instance-address.amazonaws.com: .`
10. Tip: Use `tmux` command before running a script to open a new screen. Transition back to main screen with `ctrl+b,d` and then back again using `tmux attach -d`. This allows you to log out of AWS while keeping a script running.
