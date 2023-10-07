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
                            password="****",
                            port="5432")
    db1 = conn.cursor()

    db1.execute('''SELECT "website", "title", "weblink" FROM public."scraperapp_scrapelink" ''')
    values = db1.fetchall()

    data = [{
        "website": row[0],
        "title": row[1],
        "weblink": row[2]
    } for row in values]
    
    #Autoscraper
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

    # E-mail sending
    sender_email = "daily******@gmail.com"
    sender_password = "****"
    recipient_email = "b******@gmail.com"

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
        print("E-posta gönderildi.")
    except Exception as e:
        print("E-posta gönderme hatası:", str(e))


