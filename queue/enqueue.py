from celery import Celery
from celery import Task
from celery.decorators import task
from celery.utils.log import get_task_logger

import MySQLdb
db = MySQLdb.connect(
    host= "localhost",
    user="root",
    passwd="root",
    db="test"
)

cur = db.cursor()

app = Celery('queue', broker='redis://localhost', result='redis://localhost:6379/0')
logger = get_task_logger(__name__)

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Africa/Nairobi',
    CELERY_ALWAYS_EAGER=True,
    CELERY_STORE_ERRORS_EVEN_IF_IGNORED=True,
    CELERY_ENABLE_UTC=True,
    CELERY_ANNOTATIONS = {
      'enqueue.add_stat_cost': {'rate_limit': '100/s'},
      'enqueue.add_stat_failed': {'rate_limit': '100/s'},
      'enqueue.add_stat_airtime': {'rate_limit': '100/s'},
    }
)


@app.task
def add_stat_cost(username, date, network, country, cost):
    try:
         cur.execute("""INSERT INTO bulk_sms_networks_cost VALUES(%s, %s,
             %s, %s, %s)""", (username, date, network, country, cost) )
         res = db.commit()
         logger.info(res)
         return res
    except Exception as e:
         logger.error(e)
         return e


@app.task
def add_stat_failed(username, date, network, country, failed):
    try:
         cur.execute("""INSERT INTO bulk_sms_networks_failed VALUES(%s, %s, 
             %s, %s, %s)""", (username, date, network, country, failed) )
         res = db.commit()
         logger.info(res)
         return res
    except Exception as e:
         logger.error(e)
         return e

@app.task
def add_stat_airtime(username, date, network, country, cost):
    try:
         cur.execute("""INSERT INTO airtime_networks_delivered VALUES(%s, %s, 
             %s, %s, %s)""", (username, date, network, country, cost) )
         res = db.commit()
         logger.info(res)
         return res
    except Exception as e:
         logger.error(e)
         return e
