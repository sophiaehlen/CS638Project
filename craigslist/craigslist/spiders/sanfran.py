import scrapy
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
        for link in links:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=self.parse_attr)

    def parse_attr(self, response):
        item = CraigslistItem()
        item["link"] = response.url
        item["attr"] = "".join(response.xpath("//p[@class='attrgroup']//text()").extract())
        return item
