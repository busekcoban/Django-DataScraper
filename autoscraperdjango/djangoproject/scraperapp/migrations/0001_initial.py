# Generated by Django 4.2.6 on 2023-10-05 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapeLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.TextField()),
                ('title', models.TextField()),
                ('weblink', models.TextField()),
            ],
        ),
    ]
