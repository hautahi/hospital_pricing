# Round 3 Scraping Code

The initial scraping/crawling process is divided into several rounds. This folder contains the code and output from the third round, which runs a direct google search that include terms like "chargemaster" and "price list" and then scrape those pages to 1-layer using the `scrapy` crawling framework.

## File Descriptions
- The `scrapy_price` folder and the `scrapy.cfg` file are the core structures needed for the scrapy framework. Most are created by default, except for the `search_spider.py` file in `./scrapy_price/spiders`, which defines the crawler used for this round.

- `1.google_search.py` searches google using: 'hospital-name'+'city'+ 'keywords' where 'keywords' include a number of terms related to pricing sheets. It returns the first few google hits, which are then saved to a hospital-specific csv file in the `urls` folder.

- `2.get_filelocations.py` calls the spider defined in `./scrapy_price/spiders/search_spider.py` to scrape the url location of csv/excel files 1 layer deep of the websites defined in the hospital-specific csv files in the `urls` folder. It saves the location into a hospital-specific csv file in `file_locations`.

- `urls` contains files corresponding to each hospital of the top google hits from the search run by `1.google_search.py`. The full folder can be downloaded from [here](https://www.dropbox.com/sh/msxmyhr7tcr0pmu/AAAm1q0RE5ZrCo68T_QdoOnwa?dl=0).

- `file_locations` contains files corresponding to each hospital in which the url location of the found csv/excel file is stored. The full folder can be downloaded from [here](https://www.dropbox.com/sh/v7tq3p7x219f1xa/AABzqU7Z9TXpdSdNPqojpMhYa?dl=0).
