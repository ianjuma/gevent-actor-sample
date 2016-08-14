#! /usr/bin/python

from baseService import BaseService
from queue import enqueue

from logger import logger


class AirtimeDeliveredCostService(BaseService):
    def get_view(self):
        return 'airtime/delivered?granularity=day&metric=cost&currencyCode=USD&' + \
                  'startDate={}&endDate={}'.format(self.date, self.date)

    def processResponse(self, response):
      for username in response.get('responses').get('userStats')[0].get('elements'):
          self.receive({
            'username': username,
            'date': self.date
          })

    def processUserResponse(self, response, username):
        for stat in response.get('responses').get('networkStats'):
          date = stat.get('date')

          for destination, amount in stat.get('elements').items():
              country = destination.split('(')[0].strip()
              network = destination.split('(')[1].strip("()").strip()
              cost    = amount.split(' ')[1]
 
              logger.info("{} - {} - {} - {} - {}".format(username, date, network, country, cost))
              enqueue.add_stat_airtime.delay(username, date, network, country, cost)
