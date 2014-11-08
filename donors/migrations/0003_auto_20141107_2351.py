# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0002_auto_20141107_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='phone',
            field=localflavor.us.models.PhoneNumberField(max_length=20, null=True),
            preserve_default=True,
        ),
    ]
