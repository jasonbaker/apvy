from celery.task import Task

class CronTask(Task):
    abstract=True
    type='cron'
    args=()
    kwargs={}
