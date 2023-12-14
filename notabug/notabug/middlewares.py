# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from twisted.internet.error import TCPTimedOutError, TimeoutError


class NotabugRetryMiddleware(RetryMiddleware):
    def process_exception(self, request, exception, spider):   
        if isinstance(exception, TimeoutError) or isinstance(exception, TCPTimedOutError): 
            return self._retry(request, exception, spider)
        
