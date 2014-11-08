# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('refugee_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='mailing_address',
            field=models.CharField(default='', max_length=10000, blank=True),
            preserve_default=False,
        ),
    ]
