# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('refugee_manager', '0002_volunteer_mailing_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assessment',
            options={'get_latest_by': 'date'},
        ),
    ]
