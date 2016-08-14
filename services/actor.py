import gevent
from gevent.queue import Queue


class Actor(gevent.Greenlet):
    def __init__(self):
        self.inbox = Queue() # FIFO
        gevent.Greenlet.__init__(self)

    def receive(self):
        raise NotImplemented()

    def _run(self):
        self.running = True

        while self.running:
            message = self.inbox.get()
            self.receive(message)
