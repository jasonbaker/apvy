ApVY
-------------

ApVY is an asynchronous task scheduler that is built upon twisted and interfaces
with celery.  It is intended to be largely interchangeable with celery's
built-in celerybeat scheduler (although that is definitely a work in progress).
The biggest difference is that apvy runs in a twisted event loop, making it
possible to do things such as call web tasks without having to tie up a worker
process.

Caveats
------------

ApVY is still in the proof of concept phase.

ApVY currently does not support celery's PeriodicTask interface largely due to
it working differently from twisted.scheduling's interface.  A fix for this is
planned.  You may make tasks schedulable by subclassing apvy.cron.CronTask.
Upon doing so, you must give the subclass a cron attribute which has the same
syntax as `cron <http://en.wikipedia.org/wiki/Cron#Examples>`_.  Ex::

    class MyTask(CronTask):
        cron='*/5 * * * *'
        def run(self):
            print 'Hello, world!'

FAQ
------------

Q: Why the name ApVY?

A: ApVY is a virus that causes celery to become twisted.
