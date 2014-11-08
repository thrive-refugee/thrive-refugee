# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('business', models.CharField(max_length=64, blank=True)),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('phone', models.CharField(max_length=13)),
                ('address', models.TextField(blank=True)),
                ('last_amount', models.DecimalField(max_digits=11, decimal_places=2)),
                ('last_donation', models.DateField(default=datetime.date.today)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
