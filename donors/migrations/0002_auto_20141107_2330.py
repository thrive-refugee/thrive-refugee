# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='phone',
            field=localflavor.us.models.PhoneNumberField(max_length=20),
            preserve_default=True,
        ),
    ]
