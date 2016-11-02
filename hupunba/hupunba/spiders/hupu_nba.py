import scrapy
from hupunba.items import HupunbaItem


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
            item = HupunbaItem()
            item['rank'] = response.xpath('//tr['+str(i)+']/td[1]/text()').extract()
            item['name'] = response.xpath('//tr['+str(i)+']/td[2]/a/text()').extract()
            item['team'] = response.xpath('//tr['+str(i)+']/td[3]/a/text()').extract()
            item['point'] = response.xpath('//tr['+str(i)+']/td[4]/text()').extract()
            item['fgs'] = response.xpath('//tr['+str(i)+']/td[6]/text()').extract()
            item['threefgs'] = response.xpath('//tr['+str(i)+']/td[8]/text()').extract()
            item['freethrowfgs'] = response.xpath('//tr['+str(i)+']/td[10]/text()').extract()
            item['matchnumber'] = response.xpath('//tr['+str(i)+']/td[11]/text()').extract()
            item['time'] = response.xpath('//tr['+str(i)+']/td[12]/text()').extract()
            yield item

