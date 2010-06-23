from celery.decorators import task

@task
def ping():
    print 'pong'
