import scrapy
from hupunba.items import HupunbaItem
from scrapy.http import Request


class HupuSpider(scrapy.Spider):
    name = "hupu"
    allowed_domains = ["hupu.com"]
    # start_urls = [
    #     "http://g.hupu.com/nba/stats/players/pts"
    # ]

    def start_requests(self):
        urls = []
        for i in range(1, 8):
            url = 'http://g.hupu.com/nba/stats/players/pts/%s' % i
            page = scrapy.Request(url)
            urls.append(page)
        return urls

    def parse(self, response):
        for i in range(2,52):
            urls = response.xpath('//tr['+str(i)+']/td[2]/a/@href').extract()
            for url in urls:
                yield Request(url, callback=self.parse2, dont_filter=True)

    def parse2(self, response):
        item = HupunbaItem()
        item['name'] = response.xpath('//h2/text()').extract()
        item['team'] = response.xpath('//div/div[2]/p[5]/a/text()').extract()
        item['point'] = response.xpath('//div[2]/span[2]/b/text()').extract()
        item['assist'] = response.xpath('//div[3]/span[2]/b/text()').extract()
        item['rebound'] = response.xpath('//div[4]/span[2]/b/text()').extract()
        item['fgs'] = response.xpath('//div[5]/span[2]/b/text()').extract()
        item['threefgs'] = response.xpath('//div[6]/span[2]/b/text()').extract()
        item['freethrowfgs'] = response.xpath('//div[7]/span[2]/b/text()').extract()
        item['block'] = response.xpath('//div[8]/span[2]/b/text()').extract()
        item['steal'] = response.xpath('//div[9]/span[2]/b/text()').extract()
        return item

