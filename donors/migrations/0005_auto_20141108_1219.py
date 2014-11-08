# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0004_auto_20141108_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when', models.DateField(default=datetime.date.today)),
                ('amount', models.DecimalField(max_digits=11, decimal_places=2)),
                ('memo', models.CharField(max_length=256, blank=True)),
                ('donor', models.ForeignKey(to='donors.Donor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='donor',
            name='last_amount',
        ),
        migrations.RemoveField(
            model_name='donor',
            name='last_donation',
        ),
    ]
