# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import refugee_manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('refugee_manager', '0003_auto_20141108_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=2000, blank=True)),
                ('file', models.FileField(upload_to=refugee_manager.models.case_file_upload_path)),
                ('date_uploaded', models.DateField(default=datetime.date.today)),
                ('case', models.ForeignKey(related_name='files', to='refugee_manager.Case')),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
            bases=(models.Model,),
        ),
    ]
