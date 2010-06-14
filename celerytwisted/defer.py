from threading import Event

class DeferredResult(object):
    """
    Make a result from a twisted deferred object.
    """
    def __init__(self, deferred):
        self.event = Event()
        self.deferred = deferred
        self.deferred.addCallback(self.handle_response)
        self.deferred.addErrback(self.handle_error)
        self.result = None
        self.traceback = None

    def revoke(self, *args, **kwargs):
        raise NotImplementedError, "Cannot revoke deferred results"

    def ready(self):
        return self.event.is_set()

    def unblock(self):
        """
        Unblock any threads that have called get or wait on this result.
        """
        self.event.set()

    def handle_response(self, raw_message):
        """
        The deferred's callback.
        """
        print raw_message
        message = extract_response(raw_message)
        print message
        self.result = message
        self.unblock()
        return message

    def handle_error(self, failure):
        """
        The deferred's errback.
        """
        self.result = failure.value
        self.traceback = failure.getTraceback()
        print self.traceback
        self.unblock()
        return failure

 
