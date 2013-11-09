from django.db import models

import datetime

# Create your models here.


class ESLStudent(models.Model):
    FirstName = models.CharField("First Name", max_length=50)
    LastName = models.CharField("Last Name", max_length=80)
    StreetAddress = models.CharField("Address", max_length=50)
    City = models.CharField(max_length=20)
    State = models.CharField(max_length=2)
    Zip = models.CharField(max_length=10)
    Phones = models.CharField(max_length=50, blank=True)
    Active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'ESL Student'
        verbose_name_plural = 'ESL Students'

    def __unicode__(self):
        return self.FirstName


class Attended(models.Model):
    esl_tudent = models.ForeignKey(ESLStudent)
    attend_date = models.DateField('Attended')


class Assesment(models.Model):
    esl_tudent = models.ForeignKey(ESLStudent)
    taken_date = models.DateField('Taken')
    Score = models.IntegerField()
