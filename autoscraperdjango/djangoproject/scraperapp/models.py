from django.db import models

class ScrapeLink(models.Model):
    website = models.TextField()
    title = models.TextField()
    weblink = models.TextField()
