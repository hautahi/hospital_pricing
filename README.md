# hospital_pricing

This repository contains the code for the hospital price scraping project. The folder/file descriptions are as follows:

- `round1_scrape` contains code for the first round of scraping, which was conducted using the `requests` and `Google-Search-API` python packages. A detailed description of the code is provided within that folder.

- `round2_scrape` contains code for the second round of scraping, which was conducted using the `scrapy` python framework. A detailed description of the code is provided within that folder.

- `round3_scrape` contains code for the third round of scraping, in which url's were found by including various keywords in a google search and doing a 1-layer scrape of the top google hits. A detailed description of the code is provided within that folder.


- `analysis` contains code that begins to analyze the downloaded files.

- `Hospital_General_Information.csv` is the master file of hospitals.

- `Hospital_General_Information_url.csv` is identical to the above but with three columns added that correspond to the first three google search hits (which are obtained from the `1.google_search.py` file in the `round1_scrape` folder.

- `consolidated_scraped_files` contains folders corresponding to each hospital in which the scraped files from that hospital is stored. The files are the combined attempts of the 3 rounds. There are too many files to upload here, but they can be downloaded from [this dropbox link](https://www.dropbox.com/sh/afpoveqn7elmzkn/AACTMyNvGZ3ZtCe08ualKrRba?dl=0).

## AWS Setup Instructions

All of the computations have so far been done on desktop computers. But I'm leaving this text here to remind myself of the various steps when/if we decide to implement on AWS.

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
