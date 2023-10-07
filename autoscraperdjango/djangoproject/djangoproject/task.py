from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from scraperapp.views import scrape_and_send_email


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    register_events(scheduler)
    scheduler.add_job (scrape_and_send_email, 'cron', day_of_week='mon-fri', hour=10, minute=0, id = 'scrape_and_send_email', max_instances=1, replace_existing=True)
    scheduler.start()