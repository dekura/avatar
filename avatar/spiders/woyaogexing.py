# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request
#Item Loaders提供了一种便捷的方式填充抓取到的 :Items
from urllib import parse
from avatar.items import DetailItem

class WoyaogexingSpider(scrapy.Spider):
    name = 'woyaogexing'
    allowed_domains = ['woyaogexing.com']
    start_urls = ['http://www.woyaogexing.com/touxiang/z/nvom/index.html']



    def parse(self, response):

        image_nodes = response.css('div.txList')
        for image_node in image_nodes:
            detail_url = image_node.css(' a:nth-child(1)::attr(href)').extract_first("")
            # print(detail_url)
            yield Request(url=parse.urljoin(response.url, detail_url), callback=self.parse_detail)


        next_url = response.css('.page > a:last-child::attr(href)').extract_first()
        # print(next_url)
        if next_url:
            print('正在爬取：',next_url)
            yield Request(url=parse.urljoin(response.url, next_url),callback=self.parse)


    def parse_detail(self,response):
        detail = DetailItem()
        detail['image_urls'] = response.xpath('//*[@id="main"]/div[3]/div[1]/div[1]/ul/li/a/img/@src').extract()
        # print(detail['image_urls'])
        yield detail