# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('refugee_manager', '0004_casefile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(verbose_name=b'Notes')),
                ('start_date_time', models.DateTimeField()),
                ('stop_date_time', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Name')),
                ('phone', models.CharField(max_length=80, verbose_name=b'Phone Number')),
            ],
            options={
                'verbose_name': 'Attendee',
                'verbose_name_plural': 'Attendees',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date_time', models.DateTimeField()),
                ('stop_date_time', models.DateTimeField()),
                ('members', models.ManyToManyField(to='classes.Attendee', through='classes.Attendance')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='refugee_manager.Volunteer', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WalkinClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Name')),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='session',
            name='walk_in_class',
            field=models.ForeignKey(to='classes.WalkinClass'),
            preserve_default=True,
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
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set([('attendee', 'session')]),
        ),
    ]
