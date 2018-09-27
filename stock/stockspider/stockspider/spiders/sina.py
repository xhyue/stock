# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
from selenium import webdriver                  # 导入selenium模块来操作浏览器软件
from scrapy.xlib.pydispatch import dispatcher   # 信号分发器
from scrapy import signals
from stockspider.items import TencentItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']

    
    start_urls = ['http://finance.sina.com.cn/7x24/?tag=10',
                  'http://finance.sina.com.cn/7x24/?tag=2',
                  'http://finance.sina.com.cn/7x24/?tag=3']

    def parse(self, response):
        pass


    def process_request(self, request, spider):
        content = self.selenium_request(request.url)




