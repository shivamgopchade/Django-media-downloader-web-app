# Generated by Django 3.2.7 on 2021-09-25 18:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_media_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 25, 18, 8, 25, 123222, tzinfo=utc)),
        ),
    ]
