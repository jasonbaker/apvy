from celery.task.http import (HttpDispatchTask, GET_METHODS, MutableURL, 
                              URL as BaseURL, extract_response, HttpDispatch)
from celery.exceptions import TimeoutError
from celery import states
from twisted.web.client import getPage
from twisted.python.failure import Failure

from celerytwisted.defer import DeferredResult

class TwistedHttpTask(HttpDispatchTask):
    @classmethod
    def apply_async(self, url=None, method='GET', args=None, kwargs=None, **options):
        """
        Run this task using Twisted's asynchronous HTTP client.
        """
        url = MutableURL(url or self.url)
        if method in GET_METHODS and kwargs:
            url.query.update(kwargs)
            postdata=None
        else:
            postdata=kwargs
        deferred = getPage(url=str(url), 
                           method=method,
                           postdata=postdata,
                           agent=HttpDispatch.user_agent)
        return DeferredResult(deferred)

    @classmethod
    def delay(self, url=None, method='GET', *args, **kwargs):
        return self.apply_async(url=url, method=method, args=args,
                                kwargs=kwargs)
       
class URL(BaseURL):
    dispatcher = TwistedHttpTask
