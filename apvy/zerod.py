from twisted.internet import reactor
from celery import conf
import zero.crontask
import zero.builtin_tasks
from zero.amqp import connect_to_server

def main():
    from celery.loaders import current_loader
    current_loader().init_worker()
    connect_to_server()
    reactor.run()


