# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('donors', '0005_auto_20141108_1219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donation',
            options={'ordering': ['-when'], 'get_latest_by': 'when'},
        ),
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.DecimalField(max_digits=11, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='donation',
            order_with_respect_to='donor',
        ),
    ]
