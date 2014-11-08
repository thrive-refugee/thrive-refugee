# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0003_auto_20141107_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='phone',
            field=localflavor.us.models.PhoneNumberField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
