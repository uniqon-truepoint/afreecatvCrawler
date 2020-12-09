# -*- coding: utf-8 -*-
import os
import scrapy
import requests
import re

from datetime import datetime as dt
from crawler.pipelines import Afreecacreators
from crawler.items import AfreecatvChat
from crawler.middlewares import chatAllData
from crawler.logger import logger as lg

from selenium import webdriver

from .creatorList import creatorList as cL


class AfreecatvSpider(scrapy.Spider):
    name = 'afreecatv'
    allowed_domains = ['play.afreecatv.com', 'login.afreecatv.com']

    def __init__(self, *args, **kargs):
        self.start_url = kargs['start_url']
        self.creatorId = self.start_url[26:-1]
        
        
    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse, method='GET', encoding='utf-8')

    def parse(self, response):
        # 유동성적은 데이터
        creatorName = response.xpath('//*[@id="player_area"]/div[2]/div[2]/div[1]/text()').get()
        startAt = response.xpath('//*[@id="player_area"]/div[2]/div[2]/ul/li[1]/span/text()').get()
        resolution = response.xpath('//*[@id="player_area"]/div[2]/div[2]/ul/li[2]/span/text()').get()
        videoQuality = response.xpath('//*[@id="player_area"]/div[2]/div[2]/ul/li[3]/span/text()').get()
        endAt = dt.now().strftime('%Y-%m-%d %H:%M:%S')
        afreecaCreator =  Afreecacreators()
        afreecaCreator.updateContent(self.creatorId, creatorName, startAt, resolution, videoQuality, endAt)


        lg.info(f'{creatorName}님의 채팅 데이터를 저장합니다.')

        item = AfreecatvChat()
        
        for chatData in chatAllData:
            item['text'] = chatData['text']
            item['is_mobile'] = chatData['is_mobile']
            item['sex'] = chatData['sex']
            item['grade'] = chatData['grade']
            item['chattime'] = chatData['chattime']
            item['userId'] = chatData['userId']
            item['viewer'] = chatData['viewer']
            item['category'] = chatData['category']
            item['videoTitle'] = chatData['videoTitle']
            item['like'] = chatData['like']
            item['bookmark'] = chatData['bookmark']
            item['creatorId'] = chatData['creatorId']
            yield item
        