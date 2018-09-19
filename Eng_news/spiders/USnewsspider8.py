#coding=utf-8

import re
import json
from scrapy.selector import Selector
try:
    from scrapy.spiders import Spider
except:
    from scrapy.spiders import BaseSpider as Spider
from scrapy.spiders import CrawlSpider, Rule
#from scrapy.linkextractors import LinkEx
from Eng_news.items import EngNewsItem
from Eng_news.dns_cache import _setDNSCache
import scrapy
import requests
import json

class Eng_news(CrawlSpider):
    name = "news900"
    custom_settings = { # 自定义该spider的pipeline输出
        'ITEM_PIPELINES': {
            'Eng_news.pipelines.newsPipeline900': 1,
        }
    }  
    allowed_domains = ["theguardian.com"]
    start_urls = [
    "https://www.theguardian.com/education?page=%s" % p for p in range(800, 900) # range(1,*)
    ]
    
    print("************** 我是神奇的分割线 ***************")
    
    
    def parse(self, response):       # 爬取每一个page里的每条新闻的url，并传给parse_news解析
        for href in response.xpath('.//a[@class="fc-item__link"]/@href'):
            #full_url = response.urljoin(href.extract())
            full_url = href.extract()
            yield scrapy.Request(full_url, callback = self.parse_news)
    
    def parse_news(self, response):
        _setDNSCache()
        News_item = EngNewsItem()
        # 新闻标题
        try:
            News_item['title'] = response.xpath('.//h1/text()').extract()[-1].strip()
        except:
            News_item['title'] = None
            print('Where is the title!!')
        # 新闻链接
        News_item['url'] = response.xpath('.//link[@rel="canonical"]/@href').extract()[0]
        # 新闻发布时间
        News_item['pubtime'] = response.xpath('.//time[@itemprop="datePublished"]/@datetime').extract()[0]
        # 新闻主题
        News_item['topic'] = response.xpath('.//a[@class="submeta__link"]/text()').extract_first()
        # 新闻正文 包括富文本 or 图片新闻文本 or 视频新闻文本
        News_item['main_text'] = "\n".join([i.strip() for i in response.xpath('.//div[@itemprop="articleBody"]/p/text() |.//div[@class="gallery__caption"]/text() |.//div[@class="content__standfirst"]/p/text()').extract()] )
        '''
        # 抓取动态js的评论数
        try:
            comment_url = 'https://api.nextgen.guardianapps.co.uk/discussion/comment-counts.json?shortUrls=' + response.xpath('.//div[@id="comments"]/@data-discussion-key').extract()[0]
            wbdata = requests.get(comment_url).text
            data = json.loads(wbdata)
            News_item['comment_num'] = data['counts'][0]['count']
        except:
            News_item['comment_num'] = None             # 很多新闻是没有comment的
            print('No comment number here!')
        
        # 抓取动态js的分享数
        share_url = 'https://api.nextgen.guardianapps.co.uk/sharecount/' + response.xpath('.//link[@rel="canonical"]/@href').extract()[0][28:] + '.json'
        sharedata = requests.get(share_url).text
        share_data = json.loads(sharedata)
        News_item['share_num'] = share_data['share_count']
        '''
        # 最后输出
        yield News_item

