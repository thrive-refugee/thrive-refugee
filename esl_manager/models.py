from django.db import models
import datetime

# Create your models here.

class ESLStudent(models.Model):
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=80)
    StreetAddress = models.CharField(max_length=50)
    City = models.CharField(max_length=20)
    State = models.CharField(max_length=2)
    Zip = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.FirstName

class Addended(models.Model):
    poll = models.ForeignKey(ESLStudent)
    attend_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.attend_date

