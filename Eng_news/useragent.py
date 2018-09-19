# -*-coding:utf-8-*-  
  
from scrapy import log  
  
"""避免被ban策略之一：使用useragent池。 
 
使用注意：需在settings.py中进行相应的设置。 
"""  
  
import random  
from scrapy import signals
try:
    from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware  
except:
    from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RandomUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, settings, user_agent='Scrapy'):
        super(RandomUserAgentMiddleware, self).__init__()
        self.user_agent = user_agent
        self.user_agent_list = settings.get('USER_AGENT_LIST')

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)
        crawler.signals.connect(obj.spider_opened,
                                signal=signals.spider_opened)
        return obj

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)
