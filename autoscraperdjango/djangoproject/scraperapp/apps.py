from django.apps import AppConfig
from django.conf import settings

class ScraperappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scraperapp'
    
    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from djangoproject import task
            task.start()
