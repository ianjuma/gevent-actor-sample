import datetime
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)


class Util:
    @staticmethod
    def next_date(date):

        # if date today - don't push next
        if date == datetime.datetime.now().strftime("%Y-%m-%d"):
            return date
        else:
            date_1    = datetime.datetime.strptime(date, "%Y-%m-%d")
            return str((date_1 + datetime.timedelta(days = 1))).split(' ')[0]


    @staticmethod
    def set_key(key, value):
        r.set(key, value)


    @staticmethod
    def get_key(key):
        return r.get(key)
