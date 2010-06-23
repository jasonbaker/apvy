from pkg_resources import resource_filename
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.protocol import ClientCreator
from twisted.python import log
import txamqp.spec
from txamqp.protocol import AMQClient
from txamqp.client import TwistedDelegate
from celery import conf
from celery.registry import tasks
from cPickle import loads

from zero.scheduler import Scheduler

amqp_file = resource_filename(__name__, 'amqp0-8.xml')
spec = txamqp.spec.load(amqp_file)

@inlineCallbacks
def got_connection(connection, username, password):
    print 'Connected to broker'
    yield connection.authenticate(username, password)
    print 'Authenticated'
    chan = yield connection.channel(1)
    yield chan.channel_open()

    yield chan.queue_declare(queue='zero', durable=True, exclusive=False,
                             auto_delete=False)
    yield chan.exchange_declare(exchange='zeroservice', type='direct',
                                durable=True, auto_delete=False)
    yield chan.queue_bind(queue='zero', exchange='zeroservice',
                          routing_key='zero_server')
    yield chan.basic_consume(queue='zero', no_ack=True, consumer_tag='zerotag')

    queue = yield connection.queue('zerotag')

    print 'Listening for messages'

    scheduler = Scheduler(connection)
    scheduler.schedule()

    while True:
        raw_msg = yield queue.get()
        # hack - we should really be finding out the content encoding and using
        # carrot.serializers.
        msg = loads(raw_msg.content.body)
        task = tasks[msg['task']]
        task(*msg['args'], **msg['kwargs'])

    print 'Closing connection'
    chan0 = yield connection.channel(0)
    yield chan0.connection_close()
    reactor.stop()

def connect_to_server():
    host = conf.BROKER_HOST
    port = conf.BROKER_PORT
    vhost = conf.BROKER_VHOST
    username = conf.BROKER_USER
    password = conf.BROKER_PASSWORD

    delegate = TwistedDelegate()
    d = ClientCreator(reactor, AMQClient, delegate=delegate, vhost=vhost,
                      spec=spec).connectTCP(host, int(port))
    d.addCallback(got_connection, username, password)

    def errback(err):
        if reactor.running:
            log.err(err)
            reactor.stop()
    d.addErrback(errback)
