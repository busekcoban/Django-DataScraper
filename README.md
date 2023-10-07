# Django-DataScraper
Building a Data Collection and E-mail Sending Project with Django

Data science plays a crucial role in various industries and domains today. 
It involves collecting, processing, and interpreting data to solve problems in business and daily life. 
In this blog post, we will explore how to create a data collection and email sending project using Django, step by step.

## Step 1: Creating a Django Project

In the first step, let's create a Django project named `djangoproject`. You can follow these commands:

```bash
django-admin startproject djangoproject
cd djangoproject
```

## Step 2: Creating a Django App

After creating the project, we need to add a Django app. Let's name this app scraperapp:

```bash
python manage.py startapp scraperapp
```
## Step 3: Editing the Settings File

We need to edit the Django project's settings file, settings.py. In this file, make the following changes:

```bash
INSTALLED_APPS = [
    ...
    'scraperapp',
    'django_apscheduler',
]

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"  # Default

SCHEDULER_DEFAULT = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "MyDatabase",
        "USER": "postgres",
        "PASSWORD": "******",
        "HOST": "******",
        "PORT": "5432",
    }
}
```

With these changes, we add the scraperapp app and configure Django to use a PostgreSQL database.

## Step 4: Creating a Database Table

To collect data, we need to create a database table. Define this table in the models.py file as follows:

```bash
from django.db import models

class ScrapeLink(models.Model):
    website = models.TextField()
    title = models.TextField()
    weblink = models.TextField()
```

## Step 5: Migrating Database and App Changes

After configuring the settings, we need to apply the changes to the database and the app.
These commands will create the database tables and set up the necessary tables for the django-apscheduler package.
After defining the model, apply the changes to the database using the following commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 6: Writing the Data Collection and Email Sending Function

We need to create a function to collect data and send emails. You can create this function in the scraperapp/views.py file.
If you need to understand AutoScraper principle click [here](https://pypi.org/project/autoscraper/).

```bash
import psycopg2
from autoscraper import AutoScraper
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def scrape_and_send_email():
    # PostgreSQL connection
    conn = psycopg2.connect(database="MyDatabase",
                            host="*****",
                            user="postgres",
                            password="******",
                            port="5432")
    db1 = conn.cursor()

    db1.execute('''SELECT "website", "title", "weblink" FROM public."scraperapp_scrapelink" ''')
    values = db1.fetchall()

    data = [{
        "website": row[0],
        "title": row[1],
        "weblink": row[2]
    } for row in values]
    
    # AutoScraper
    scraper = AutoScraper()

    total = []

    for item in data:
        url = item['website']
        wanted_title = [item['title']]
        wanted_weblink = [item['weblink']]

        resulttitle = scraper.build(url, wanted_title)
        resultweblink = scraper.build(url, wanted_weblink)

        for title, weblink in zip(resulttitle, resultweblink):
            total.append((title, weblink))

    # Email sending
    sender_email = "daily****@gmail.com"
    sender_password = "xxx"
    recipient_email = "b****@gmail.com"

    subject = "Scraped Daily News"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    body = "Good morning, here it's the daily news\n\n"
    for title, weblink in total:
        body += f"{title}\nLink: {weblink}\n\n"

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent.")
    except Exception as e:
        print("Email sending error:", str(e))
```

Note that you need to set app password to send e-mail automatically.

## Step 7: Setting Up the Task

To schedule and automate the task, we need to create a task.py file in the project's root directory. Use the following code to set up the task:

```bash
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from scraperapp.views import scrape_and_send_email

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    register_events(scheduler)
    scheduler.add_job (scrape_and_send_email, 'cron', day_of_week='mon-fri', hour=10, minute=0, id = 'scrape_and_send_email', max_instances=1,replace_existing=True)
    scheduler.start()
```

## Step 8: Configuring the AppConfig

Finally, in the scraperapp/apps.py file, add the following code to configure the app:

```bash
from django.apps import AppConfig
from django.conf import settings

class ScraperappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scraperapp'
    
    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from djangoproject import task
            task.start()
```
## Step 9: Add some data to table

To test the job, we need to add some data to "scraperapp_scrapelink" table. 

```sql
INSERT INTO
public."scraperapp_scrapelink"("website", "title", "weblink")
VALUES
('https://edition.cnn.com/business/tech','Apple rejected opportunities to buy Microsoft’s Bing, integrate with DuckDuckGo','https://edition.cnn.com/2023/10/05/tech/apple-microsoft-bing-duckduckgo-google-search/index.html'),
('https://www.theguardian.com/world','UN investigation into Tigray abuses to end despite reports of more atrocities','https://www.theguardian.com/world/2023/oct/04/un-investigation-into-tigray-abuses-to-end-despite-reports-of-more-atrocities');
```

## Step 10: Running the Project

Now, let's create an admin user to access the Django admin interface:

```bash
python manage.py createsuperuser
```

Follow the prompts to create the superuser account. After that, run the server:

```bash
python manage.py runserver
```

Access the Django admin interface at http://127.0.0.1:8000/admin/. You can view and manage the scheduled job we created in the Django jobs section. The job is set to run every weekday at 10 AM by default.
That's it! You have successfully built a data collection and email sending project using Django. This project can be customized and expanded for various data collection and reporting tasks.

Happy coding!
