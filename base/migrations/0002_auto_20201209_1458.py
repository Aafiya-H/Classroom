# Generated by Django 3.1.3 on 2020-12-09 14:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignments',
            name='due_time',
            field=models.TimeField(default=datetime.time(10, 10)),
        ),
    ]
