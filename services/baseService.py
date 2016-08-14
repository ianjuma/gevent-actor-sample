#! /usr/bin/python

import gevent
import settings
import requests

import gevent.monkey
gevent.monkey.patch_socket()
requests.adapters.DEFAULT_RETRIES = 5

from logger import logger

from actor import Actor
from urllib import urlencode
from requests.exceptions import Timeout


class BaseService(Actor):
    base_url = settings.base_url
    date     = ''

    def build_url(self, username = None):
        if username is None:
            return self.base_url + self.get_view()
        else:
            f = { 'username': username }
            return self.base_url + self.get_view() + "&" + urlencode(f)

    def fetch_(self, url):
        headers = { 'apikey': settings.api_key }

        try:
            # reporting to snoop - re-run
            r = requests.get(url, headers = headers, timeout=120)
            resp = r.json()
            return resp
        except Timeout as e:
            logger.error('timeout exception as {}'.format(e))
            raise e
        except Exception as ex:
            logger.error('other exception as {}'.format(ex))
            raise ex

    def receive(self, message):
        username  = message.get('username')
        self.date = message.get('date')

        if username is not None:
            thread = gevent.spawn( self.fetch_,  self.build_url(username = username) )
            thread.join()
            gevent.sleep(0)

            return self.processUserResponse( thread.value, username )
        else:
            thread = gevent.spawn( self.fetch_,  self.build_url(username = None) )
            thread.join()
            gevent.sleep(0)

            return self.processResponse( thread.value )

    def get_view(self):
        raise NotImplemented

    def processResponse(self, response):
        raise NotImplemented

    def processUserResponse(self, response):
        raise NotImplemented
