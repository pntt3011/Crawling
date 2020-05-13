from scrapy import Spider, Request
from scrapy.selector import Selector
from crawler.items import CrawlerItem
import json

class CrawlerSpider(Spider):
    name = 'crawler'
    allowed_domains = ["ani4u.org"]
   
    def start_requests(self):
        url = "http://ani4u.org/list-anime"
        yield Request(url = url, callback = self.follow)
    
    def follow(self, response):
        animes = response.xpath('/html/body/div[4]/div[1]/div/div/div[1]/div/ul/li')
        for anime in animes:
            link = anime.xpath('a/@href').get()
            yield Request(url = link, callback = self.parse)
            
    def parse(self, response):
        lists = Selector(response).xpath('//div[@class="data"]')
        for anime in lists:
            item = CrawlerItem()
            item['Name'] = json.dumps(anime.xpath('h1/text()').get())
            genre_list = anime.xpath('p[2]/a/text()').getall()
            item['Genre'] = ', '.join(genre_list[1:])
            item['Year'] = anime.xpath('p[4]/a[2]/text()').get() if len(anime.xpath('p[4]/a')) > 1 else anime.xpath('p[4]/a/text()').get()
            item['Url'] = anime.xpath('a/@href').get()
            yield item

class SuperSpider(Spider):
    name = 'super'
    allowed_domains = ["ani4u.org"]
   
    def start_requests(self):
        url = "http://ani4u.org/xem-anime/bungaku-shoujo-memoire"
        yield Request(url = url, callback = self.parse)
        
    def parse(self, response):
        lists = Selector(response).xpath('//div[@class="data"]')
        for anime in lists:
            item = CrawlerItem()
            item['Name'] = anime.xpath('h1/text()').get()
            genre_list = anime.xpath('p[2]/a/text()').getall()
            item['Genre'] = ', '.join(genre_list[1:])
            item['Year'] = anime.xpath('p[4]/a[2]/text()').get() if len(anime.xpath('p[4]/a')) > 1 else anime.xpath('p[4]/a/text()').get()
            item['Url'] = anime.xpath('a/@href').get()
            yield item