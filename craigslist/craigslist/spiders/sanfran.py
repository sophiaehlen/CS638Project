import scrapy
import urllib2
import os
from scrapy import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from craigslist.items import CraigslistItem

from scrapy import Spider, Request

class SanFranSpider(BaseSpider):
    name = "craig"
    allowed_domains = ["craigslist.org"]
    start_urls = ["http://sfbay.craigslist.org/search/sfc/cto"]

    BASE_URL = 'http://sfbay.craigslist.org/'
    
    


    def parse(self, response):
        links = response.xpath("//span[@class='pl']/a/@href").extract()
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        i = 0
        for link in links:
            absolute_url = self.BASE_URL + link
            page = urllib2.urlopen(absolute_url)
            page_content = page.read()
            i += 1
            filename = os.path.join(fileDir, 'htmldata/page_content_sf_'+str(i)+'.html')
            with open(filename, 'w') as fid:
                fid.write(page_content)
            yield scrapy.Request(absolute_url, callback=self.parse_attr)

    def parse_attr(self, response):
        item = CraigslistItem()
        item["link"] = response.url
        item["title"] = "".join(response.xpath("//*[@id='titletextonly']//text()").extract())
        itemstring = "".join(response.xpath("//p[@class='attrgroup']//text()").extract())
        item["attr"] = itemstring

        unmodded_price = "".join(response.xpath("//*[@id='pagecontainer']/section/h2/span[2]/span[2]//text()").extract())
        price = unmodded_price.strip('$')
        item["price"] = price

        item["location"] = "".join(response.xpath("//*[@id='pagecontainer']/section/h2/span[2]/small//text()").extract())
        item["postbody"] = "".join(response.xpath("//*[@id='postingbody']//text()").extract())

        posted = "".join(response.xpath("//*[@id='display-date']/time/@datetime").extract())


        item["postdate"] = posted

        return item
