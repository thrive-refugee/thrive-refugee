# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import refugee_manager.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('description', models.TextField(max_length=10000)),
                ('minutes', models.IntegerField(null=True, verbose_name=b'Time spent in minutes', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('language_skills', models.IntegerField(default=0, verbose_name=b'Language Skills (highest level adult)', choices=[(0, b'0 - Please Select'), (1, b'1 - No English'), (2, b'2 - Few phrases such as yes and thank you'), (3, b'3 - Can answer a few questions'), (4, b'4 - Able to have some basic skills- knows some nouns and verbs'), (5, b'5 - Able to have basic conversation in some concrete areas'), (6, b'6 - Able to have more than basic conversation- knows various tenses, etc.'), (7, b'7 - Able to have in depth conversations around daily events'), (8, b'8 - Able to have discussions around abstract concepts'), (9, b'9 - Fluent other than some technical terms'), (10, b'10 - Fluent, including in specialty areas')])),
                ('language_skills_note', models.TextField(max_length=10000, verbose_name=b'Notes', blank=True)),
                ('employment', models.IntegerField(default=0, null=True, verbose_name=b'Employment (wage earning parent)', choices=[(0, b'0 - Please Select'), (1, b'1- Has no current job or past experience, does not want work'), (2, b'2- Desires employment but has no current or past work experience'), (3, b'3- Desires employment but has no current job, has some past experience'), (4, b'4- Desires employment, has past experience and is actively seeking'), (5, b'5- Has part time employment, low paying low skill position'), (6, b'6- Has part time position, skilled position'), (7, b'7- Has full time employment, low paying low skill position'), (8, b'8- Has full time employment in skilled position but desires another position'), (9, b'9- Has full time skilled position, is happy with pay and position'), (10, b'10- Has full time professional or highly skilled position, is fulfilled with work')])),
                ('employment_note', models.TextField(max_length=10000, verbose_name=b'Notes', blank=True)),
                ('finances', models.IntegerField(default=0, null=True, verbose_name=b'Finances (family)', choices=[(0, b'0 - Please Select'), (1, b'1- Has no employment income or DHS assistance'), (2, b'2- Has no employment, some DHS assistance but insufficient for rent'), (3, b'3- Has no employment, some DHS assistance but insufficient for needs'), (4, b'4- Has minimal employment and/ or DHS but unable to meet basic needs'), (5, b'5- Has minimal employment and/ or DHS, able to meet basic needs only'), (6, b'6- Has employment and/ or DHS, able to meet needs and has minimal extra money'), (7, b'7- Has employment and able to meet basic needs WITHOUT DHS assistance'), (8, b'8- Has employment and able to meet more than basic needs WITHOUT DHS assistance'), (9, b'9- Has employment, able to go above basic needs without assistance'), (10, b'10- Has employment and financially stable')])),
                ('finances_note', models.TextField(max_length=10000, verbose_name=b'Notes', blank=True)),
                ('transportation', models.IntegerField(default=0, null=True, verbose_name=b'Transportation (family)', choices=[(0, b'0 - Please Select'), (1, b'1- No transportation, no knowledge of bus line'), (2, b'2- No transportation, has been introduced to bus line but unwilling or unable to use'), (3, b'3- Minimal transportation, able to use bus line to few selected locations'), (4, b'4- Low level transportation, able to use bus line to some locations, has friends to transport at times, able to get to most appointments alone'), (5, b'5- Able to use bus proficiently, able to get to appointments/work, has transportation network'), (6, b'6- Able to network to get to appointments/work as needed, no driving experience'), (7, b'7- Able to get to appointments/work, desires to learn how to drive and has some experience'), (8, b'8- Some driving experience, working towards license'), (9, b'9- Has license but no car'), (10, b'10- Has license and car, able to transport self and family independently')])),
                ('transportation_note', models.TextField(max_length=10000, verbose_name=b'Notes', blank=True)),
                ('housing', models.IntegerField(default=0, null=True, verbose_name=b'Housing (family)', choices=[(0, b'0 - Please Select'), (1, b'1- Homeless'), (2, b'2- Has temporary housing'), (3, b'3- Has somewhat stable housing- month to month/ long term temporary, etc.'), (4, b'4- Has apartment but inadequate for family needs and size'), (5, b"5- Has stable apartment that is adequate, but family doesn't like area or cost"), (6, b'6- Has stable apartment, good area and cost'), (7, b'7- Has stable apartment, looking to move to better area or purchase home'), (8, b'8- In process of purchasing home'), (9, b'9- In own home, difficulties with size or mortgage'), (10, b'10- In own home, appropriate size and monthly mortgage')])),
                ('housing_note', models.TextField(max_length=10000, verbose_name=b'Notes', blank=True)),
                ('access_to_services', models.IntegerField(default=0, null=True, verbose_name=b'Access to services and health care (family)', choices=[(0, b'0 - Please Select'), (1, b'1- No access to service or health care'), (2, b'2- Minimal access to emergency services (E.R.)'), (3, b'3- Minimal access to services beyond E.R.'), (4, b'4- Has access to some minimal health care'), (5, b'5- Has access to basic health care, one or two area services with assistance'), (6, b'6- Has access to basic services without help, able to get to appointments'), (7, b'7- Has access to services that will progress family with assistance'), (8, b'8- Has access to services that will progress family without assistance'), (9, b'9- Able to research and access services on own to support family and meet most needs'), (10, b'10- Has skills to access and research services and health care independently')])),
                ('access_to_services_note', models.TextField(max_length=10000, verbose_name=b'Notes', blank=True)),
                ('education_or_training', models.IntegerField(default=0, null=True, verbose_name=b'School/ Education/ Job Training (parents)', choices=[(0, b'0 - Please Select'), (1, b'1- No school or education in home country or here, no job training'), (2, b'2- Primary school education, no job training'), (3, b'3- Middle school education, no job training'), (4, b'4- High school or above equivalent education, no job training'), (5, b'5- Some schooling, basic job training skills'), (6, b'6- Some schooling, multiple job trainings or skills'), (7, b'7- Some schooling, advanced job training or skills'), (8, b'8- Advanced job training or some college'), (9, b'9- Advanced professional training or college degree'), (10, b'10- Advanced professional training or advanced college degree')])),
                ('education_or_training_note', models.TextField(max_length=10000, verbose_name=b'Notes', blank=True)),
                ('support_of_children', models.IntegerField(default=0, null=True, verbose_name=b'Support of Children (parents)', choices=[(0, b'0 - Please Select'), (1, b'1- In need of parenting training, CPS involved, children may be in danger'), (2, b'2- In need of parenting training, CPS involved, children appear safe'), (3, b'3- In need of parenting skills, CPS may be involved, but parents want to support children'), (4, b'4- In need of parenting skills or training to understand American schools, no CPS involvement, parents attempt to support children'), (5, b'5- Some understanding of American school, parents need additional support, parents attempt to support children'), (6, b'6- Parents need support, but have some ability to support children, attend conferences, can help with homework and understand school systems'), (7, b'7- Parents able to support children in school with a minimum of support, can provide emotional support, help with homework, etc.'), (8, b'8- Parents able to support children in school, provide recreational activities and emotional support'), (9, b'9- Parents able to support children in most areas with minimal support from others'), (10, b'10- Parents able to fully support children at home and in school')])),
                ('support_of_children_note', models.TextField(max_length=10000, verbose_name=b'Notes', blank=True)),
                ('mental_health', models.IntegerField(default=0, null=True, verbose_name=b'Mental Health (all family members)', choices=[(0, b'0 - Please Select'), (1, b'1- Many family members have serious mental health difficulties, many need occasional hospitalization, not receiving needed mental health care'), (2, b'2- Many family members have serious mental health difficulties, many need occasional hospitalization, not receiving needed mental health care'), (3, b'3- One family member has serious mental health difficulties, and others may have minor difficulties, not receiving needed mental health care'), (4, b'4- One family member has serious mental health difficulties, and others may have minor difficulties, is receiving services needed'), (5, b'5- One family member has serious mental health difficulties, and others may have minor difficulties, is receiving services needed'), (6, b'6- One family member has serious mental health difficulties but is receiving interventions'), (7, b'7- One family member has moderate mental health difficulties but is receiving interventions'), (8, b'8- One family member has mild mental health difficulties but is receiving interventions'), (9, b'9- Family members appear to be in good mental health but may occasionally have stress or acculturation difficulties'), (10, b'10- Family members all appear to be in excellent mental health')])),
                ('mental_health_note', models.TextField(max_length=10000, verbose_name=b'Notes', blank=True)),
                ('social_support', models.IntegerField(default=0, null=True, verbose_name=b'Social Support (family)', choices=[(0, b'0 - Please Select'), (1, b'1- Has no social support, friends, etc.'), (2, b'2- Only has social support from one agency or program'), (3, b'3- Has social support from family members in household'), (4, b'4- Only has social support from various agencies and/ or multiple household members'), (5, b'5- Has support from one family member outside of the home or one friend'), (6, b'6- Has support from more than one friend or outside family members'), (7, b'7- Has support from multiple friends or family, participates in at least one social activity (church, support group, sewing club)'), (8, b'8- Has support from multiple friends and family, actively involved in multiple settings'), (9, b'9- Actively involved in the community'), (10, b'10- Actively involved in the community and leads some activities')])),
                ('social_support_note', models.TextField(max_length=10000, verbose_name=b'Notes', blank=True)),
                ('case_summary', models.TextField(max_length=10000, blank=True)),
                ('goals', models.TextField(max_length=10000, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=2000)),
                ('start', models.DateField(default=datetime.date.today)),
                ('end', models.DateField(null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('arrival', models.DateField(null=True, blank=True)),
                ('address', models.TextField(max_length=10000, blank=True)),
                ('phone', models.CharField(max_length=2000, blank=True)),
                ('goals', models.TextField(max_length=10000, blank=True)),
                ('employment', models.CharField(max_length=2000, blank=True)),
                ('english_classes', models.CharField(max_length=2000, blank=True)),
                ('origin', models.CharField(max_length=2000, blank=True)),
                ('language', models.CharField(max_length=2000, blank=True)),
                ('green_card', models.CharField(max_length=2000, blank=True)),
                ('dhs_worker', models.CharField(max_length=2000, blank=True)),
                ('school', models.CharField(max_length=2000, blank=True)),
                ('doctor', models.CharField(max_length=2000, blank=True)),
                ('other1', models.CharField(max_length=2000, verbose_name=b'Other', blank=True)),
                ('other2', models.CharField(max_length=2000, verbose_name=b'Other', blank=True)),
                ('other3', models.CharField(max_length=2000, verbose_name=b'Other', blank=True)),
                ('other4', models.CharField(max_length=2000, verbose_name=b'Other', blank=True)),
                ('other5', models.CharField(max_length=2000, verbose_name=b'Other', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CaseDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(max_length=10000)),
                ('case', models.ForeignKey(related_name='notes', to='refugee_manager.Case')),
            ],
            options={
                'verbose_name': 'Case Detail',
                'verbose_name_plural': 'Additional Case Details',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=2000)),
                ('relation', models.CharField(max_length=100, blank=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('medicaid', models.CharField(max_length=2000, blank=True)),
                ('ssn', models.CharField(max_length=2000, verbose_name=b'SSN', blank=True)),
                ('case', models.ForeignKey(related_name='individuals', to='refugee_manager.Case')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=255)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Volunteer Info',
                'verbose_name_plural': 'Volunteer Info',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='case',
            name='volunteers',
            field=models.ManyToManyField(to='refugee_manager.Volunteer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assessment',
            name='case',
            field=models.ForeignKey(related_name='assessment', to='refugee_manager.Case'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activitynote',
            name='case',
            field=models.ForeignKey(related_name='activity', to='refugee_manager.Case'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activitynote',
            name='volunteer',
            field=models.ForeignKey(related_name='activity', to='refugee_manager.Volunteer'),
            preserve_default=True,
        ),
    ]
