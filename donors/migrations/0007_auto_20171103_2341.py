# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-03 23:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0006_auto_20141108_1246'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donation',
            options={'get_latest_by': 'when'},
        ),
        migrations.AlterField(
            model_name='donor',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
