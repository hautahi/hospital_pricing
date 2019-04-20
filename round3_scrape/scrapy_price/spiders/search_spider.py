"""
Spider designed to extract csv/excel files located on provided websites.
This is called from the `2.get_filelocations.py` file.
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
import scrapy
import time
import pandas as pd

class file_search(CrawlSpider):
    name = 'file_search'

    # Specify rules for spider.
    rules = (
        # Links to csv files should be thrown to the parse_items method.
        Rule(LinkExtractor(allow=("\.xls","\.xlsx","\.csv","\.XLS","\.CSV","\.XLSX","get$"),deny_extensions = ("jpg","png")),callback="parse_items",follow=False),
        
    )

    # These can be overwritten at the command line using the "-s" flag too. (eg. -s FEED_URI=tmp/downloads.csv)
    custom_settings = {
       'DEPTH_LIMIT' : 1
    }

    # Put stuff in here that we want read from the command line
    def __init__(self, *args, **kwargs):
        super(file_search, self).__init__(*args, **kwargs)
        
        # Read the url list from the temp file created in 2.get_filelocations.py
        d = pd.read_csv("temp_urls.csv")
        self.start_urls = d['urls'].tolist()
        
        # Read the allowed domain list from the temp file
        d = pd.read_csv("temp_doms.csv")
        self.allowed_domains = d['doms'].tolist()
    
    # Callback function for links with desired formats like 'csv', 'xls'
    def parse_items(self, response):
        
        # Saved information
        scraped_info = {
                'file_urls': [response.urljoin(response.url)],
                'time': time.strftime("%m %d %Y %H:%M:%S", time.localtime()),
                }

        return(scraped_info)
