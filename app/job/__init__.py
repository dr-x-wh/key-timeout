import atexit
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler: Optional[BackgroundScheduler] = None


def run_job():
    global scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler(daemon=True)

        from app.job.key_timeout import run as run_key_timeout
        scheduler.add_job(func=run_key_timeout, trigger=CronTrigger(minute=0), id='run_key_timeout',
                          replace_existing=True)

        scheduler.start()

        atexit.register(lambda: scheduler.shutdown())
