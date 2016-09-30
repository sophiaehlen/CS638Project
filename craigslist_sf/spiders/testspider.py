from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from craigslist_sf.items import CraigslistSfItem

class MySpider(BaseSpider):
        name = "craig"
        allowed_domains = ["craigslist.org"]
        start_urls = ["http://sfbay.craigslist.org/search/sfc/cto"]

        def parse(self, response):
                hxs = HtmlXPathSelector(response)
                titles = hxs.select("//span[@class='pl']")
                for titles in titles:
                    item = CraigslistSfItem()
                    title = titles.select("a/text()").extract()
                    link = titles.select("a/@href").extract()
                    print(title, link)
                    #items.append(item)
                #return items
