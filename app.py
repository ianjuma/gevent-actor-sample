#! /usr/bin/python

import gevent
import logging
import time
import settings

from apscheduler.schedulers.gevent        import GeventScheduler
from services.bulkSMSCostService          import BulkSMSCostService
from services.bulkSMSFailedService        import BulkSMSFailedService
from services.airtimeDeliveredCostService import AirtimeDeliveredCostService

from util.util import Util
from services.logger import logger

sched = GeventScheduler()


class App:

    @staticmethod
    def run():
        date = Util.get_key('CrunchDate')
        next_date = Util.next_date(date)
        Util.set_key('CrunchDate', next_date)

        bulkFailed  = BulkSMSFailedService()
        bulkSuccess = BulkSMSCostService()
        airtime     = AirtimeDeliveredCostService()

        stat = { 'date': date, 'username': None }
        bulkFailed.start()
        bulkSuccess.start()
        airtime.start()

        bulkFailed.inbox.put(stat)
        bulkSuccess.inbox.put(stat)
        airtime.inbox.put(stat)

        # gevent.joinall([ bulkFailed, bulkSuccess, airtime ])


if __name__ == '__main__':
    logging.basicConfig()

    sched.add_job(App.run, 'interval', seconds=30, id='stats')
    g = sched.start()

    try:
        while True:
            g.join()
    except (KeyboardInterrupt, SystemExit, Exception, MemoryError) as e:
        logger.error('crashed as {}'.format(e))
        sched.shutdown()
