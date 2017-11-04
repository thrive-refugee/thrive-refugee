# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=50, verbose_name=b'Name')),
                ('Phone', models.CharField(max_length=80, verbose_name=b'Phone Number')),
            ],
            options={
                'verbose_name': 'Attendee',
                'verbose_name_plural': 'Attendee',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('members', models.ManyToManyField(to='classes.Attendee', through='classes.Attendance')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='attendance',
            name='attendee',
            field=models.ForeignKey(to='classes.Attendee'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendance',
            name='session',
            field=models.ForeignKey(to='classes.Session'),
            preserve_default=True,
        ),
    ]
