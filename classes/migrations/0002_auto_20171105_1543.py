# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='notes',
            field=models.TextField(verbose_name=b'Notes', blank=True),
            preserve_default=True,
        ),
    ]
