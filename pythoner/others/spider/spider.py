#encoding:utf-8
from apscheduler.scheduler import Scheduler
scheduler = Scheduler()

def test():
    print 'hello'

scheduler.deamonic = False
scheduler.add_cron_job(test,second='*/5')
scheduler.start()
