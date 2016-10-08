import scrapy
from scrapy import Selector
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from craigslist.items import CraigslistItem

from scrapy import Spider, Request
import re

class SanFranSpider(BaseSpider):
    name = "craig"
    allowed_domains = ["craigslist.org"]
    start_urls = ["http://sfbay.craigslist.org/search/sfc/cto"]

    BASE_URL = 'http://sfbay.craigslist.org/'

    def start_requests(self):
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=100', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=200', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=300', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=400', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=500', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=600', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=700', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=800', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=900', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=1000', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=1100', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=1200', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=1300', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=1400', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=1500', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=1600', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=1700', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=1800', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=1900', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=2000', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=2100', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=2200', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=2300', self.parse)
        yield scrapy.Request('http://sfbay.craigslist.org/search/sfc/cto?s=2400', self.parse)

    def parse(self, response):
        links = response.xpath("//span[@class='pl']/a/@href").extract()
        for link in links:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=self.parse_attr)

    def parse_attr(self, response):
        item = CraigslistItem()
        item["link"] = response.url
        item["title"] = "".join(response.xpath("//*[@id='titletextonly']//text()").extract())


        attributes = "".join(response.xpath("//p[@class='attrgroup']//text()").extract())
        attributes_split = attributes.split("\n")
        item["makemodel"] = attributes_split[1].lstrip()

        # Not elegant by any means, but it works
        for i in attributes_split:
            if "fuel" in i:
                fuel = i.lstrip()
                fuel = fuel[6:]
                item["fuel"] = fuel
            if "condition" in i:
                condition = i.lstrip()
                condition = condition[11:]
                item["condition"] = condition
            if "VIN" in i:
                vin = i.lstrip()
                vin = vin[5:]
                item["vin"] = vin
            if "odometer" in i:
                odometer = i.lstrip()
                odometer = odometer[10:]
                item["odometer"] = odometer
            if "drive" in i:
                drive = i.lstrip()
                drive = drive[:]
                item["drive"] = drive[7:]
            if "paint" in i:
                paint = i.lstrip()
                paint = paint[13:]
                item["paint_color"] = paint
            if "cylinders" in i:
                cylinders = i.lstrip()
                cylinders = cylinders[11:-10]
                item["cylinders"] = cylinders
            if "size" in i:
                size = i.lstrip()
                size = size[6:]
                item["size"] = size
            if "status" in i:
                tstatus = i.lstrip()
                tstatus = tstatus[14:]
                item["title_status"] = tstatus


        unmodded_price = "".join(response.xpath("//*[@id='pagecontainer']/section/h2/span[2]/span[2]//text()").extract())
        price = unmodded_price.strip('$')
        item["price"] = price

        location = "".join(response.xpath("//*[@id='pagecontainer']/section/h2/span[2]/small//text()").extract())
        location.lstrip()
        location = location[2:-1]
        item["location"] = location

        body = "".join(response.xpath("//*[@id='postingbody']//text()").extract())
        body = body.replace("\n", " ").replace(",", "").replace("  ", " ").lstrip().rstrip()
        item["postbody"] = body

        posted = "".join(response.xpath("//*[@id='display-date']/time/@datetime").extract())


        item["postdate"] = posted

        return item
