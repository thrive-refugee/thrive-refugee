from django.db import models
from django.contrib.auth.models import User

from datetime import date


# https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users
class Volunteer(models.Model):
    user = models.OneToOneField(User)

    phone = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Volunteer Info'
        verbose_name_plural = 'Volunteer Info'

    def __unicode__(self):
        if self.user.is_active:
            inactive = ''
        else:
            inactive = 'INACTIVE - '
        return '%s %s (%s%s)' % (self.user.first_name, self.user.last_name,
                                 inactive, self.user.username)


class Case(models.Model):
    volunteers = models.ManyToManyField(Volunteer)

    name = models.CharField(max_length=2000)
    start = models.DateField(default=date.today)
    end = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    arrival = models.DateField(null=True, blank=True)
    employment = models.CharField(max_length=2000, blank=True)
    english_classes = models.CharField(max_length=2000, blank=True)
    origin = models.CharField(max_length=2000, blank=True)
    language = models.CharField(max_length=2000, blank=True)
    green_card = models.CharField(max_length=2000, blank=True)
    dhs_worker = models.CharField(max_length=2000, blank=True)
    school = models.CharField(max_length=2000, blank=True)
    doctor = models.CharField(max_length=2000, blank=True)

    def __unicode__(self):
        if self.active:
            return self.name
        else:
            return '%s (closed)' % self.name


class Individual(models.Model):
    case = models.ForeignKey(Case, related_name='individuals')
    name = models.CharField(max_length=2000)
    relation = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    medicaid = models.CharField(max_length=2000, blank=True)
    ssn = models.CharField(max_length=2000, blank=True)

    def __unicode__(self):
        return '%s %s %s' % (self.name, self.relation, self.date_of_birth)