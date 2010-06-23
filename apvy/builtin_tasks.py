import sys

from celery.decorators import task

@task
def ping():
    print 'pong'

@task
def halt():
    print 'Stopping apvyd'
    sys.exit(0)
