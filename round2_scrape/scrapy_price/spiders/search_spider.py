"""
Spider designed to find the location of csv/excel files three layers deep into a provided website.
This is called from the `1.get_filelocations.py` file.
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
import scrapy
import time

class file_search(CrawlSpider):
    name = 'file_search'

    # Specify rules for spider.
    rules = (
        # Links ending with "pdf" should be thrown to the parse_items method.
        Rule(LinkExtractor(allow=("\.xls","\.xlsx","\.csv","\.XLS","\.CSV","\.XLSX","get$"),deny_extensions = ("jpg","png")),callback="parse_items",follow=False),
        
        # All links should be followed.
        # Duplicates from above rule won't be followed, which is fine because those above are just files
        Rule(LinkExtractor(allow=("", ),deny_extensions = ("jpg","png")), follow = True),
    )

    # These can be overwritten at the command line using the "-s" flag too. (eg. -s FEED_URI=tmp/downloads.csv)
    custom_settings = {
       'DEPTH_LIMIT' : 3
    }

    # Put stuff in here that we want read from the command line
    def __init__(self, *args, **kwargs):
        super(file_search, self).__init__(*args, **kwargs)
        
        # Hospital name
        self.hospital = kwargs.get('hospital')

        # Declare the start url and allowed domains from inputs
        self.allowed_domains = [kwargs.get('all_dom')] 
        self.start_urls = [kwargs.get('url')]
    
    # Callback function for links with desired formats like 'csv', 'xls'
    def parse_items(self, response):
        
        # Saved information
        scraped_info = {
                'hospital': self.hospital,
                'file_urls': [response.urljoin(response.url)],
                'time': time.strftime("%m %d %Y %H:%M:%S", time.localtime()),
                'depth' : response.meta["depth"]
                }

        return(scraped_info)
