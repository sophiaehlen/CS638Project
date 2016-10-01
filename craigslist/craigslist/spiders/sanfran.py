import scrapy
from scrapy import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from craigslist.items import CraigslistItem

class SanFranSpider(BaseSpider):
       name = "craig"
       allowed_domains = ["craigslist.org"]
       start_urls = ["http://sfbay.craigslist.org/search/sfc/cto"]

       def parse(self, response):
               hxs = HtmlXPathSelector(response)
               titles = hxs.select("//span[@class='pl']")
               for titles in titles:
                   item = CraigslistItem()
                   title = titles.select("a/text()").extract()
                   link = titles.select("a/@href").extract()
                   print(title, link)