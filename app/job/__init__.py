import atexit
import logging
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

scheduler: Optional[BackgroundScheduler] = None


def run_job():
    global scheduler
    if scheduler is None:
        logger = logging.getLogger("apscheduler")
        scheduler = BackgroundScheduler(daemon=True)

        from app.job.key_timeout import run as run_key_timeout
        scheduler.add_job(func=run_key_timeout, trigger=IntervalTrigger(minutes=1), id='run_key_timeout',
                          replace_existing=True)

        from app.job.power_outage import run as run_power_outage
        scheduler.add_job(func=run_power_outage, trigger=IntervalTrigger(minutes=1), id='run_power_outage',
                          replace_existing=True)

        scheduler.start()
        logger.info("job is running")

        atexit.register(lambda: scheduler.shutdown())
