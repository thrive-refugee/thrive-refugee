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
    address = models.TextField(max_length=10000, blank=True)
    phone = models.CharField(max_length=2000, blank=True)
    goals = models.TextField(max_length=10000, blank=True)
    employment = models.CharField(max_length=2000, blank=True)
    english_classes = models.CharField(max_length=2000, blank=True)
    origin = models.CharField(max_length=2000, blank=True)
    language = models.CharField(max_length=2000, blank=True)
    green_card = models.CharField(max_length=2000, blank=True)
    dhs_worker = models.CharField(max_length=2000, blank=True)
    school = models.CharField(max_length=2000, blank=True)
    doctor = models.CharField(max_length=2000, blank=True)
    other1 = models.CharField('Other', max_length=2000, blank=True)
    other2 = models.CharField('Other', max_length=2000, blank=True)
    other3 = models.CharField('Other', max_length=2000, blank=True)
    other4 = models.CharField('Other', max_length=2000, blank=True)
    other5 = models.CharField('Other', max_length=2000, blank=True)

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
    ssn = models.CharField('SSN', max_length=2000, blank=True)

    def __unicode__(self):
        return '%s %s %s' % (self.name, self.relation, self.date_of_birth)


class CaseDetail(models.Model):
    case = models.ForeignKey(Case, related_name='notes')
    text = models.TextField(max_length=10000)

    def __unicode__(self):
        return 'Additional Detail'

    class Meta:
        verbose_name = 'Case Detail'
        verbose_name_plural = 'Additional Case Details'


class ActivityNotes(models.Model):
    case = models.ForeignKey(Case, related_name="activity")
    volunteer = models.ForeignKey(Volunteer, related_name='activity')

    date = models.DateField(auto_now=True)
    description = models.CharField(max_length=2000)
    minutes = models.IntegerField("Time spent in minutes", blank=True)


class Assessment(models.Models):
    LANGUAGE_CHOICES =(
(1, "No English"),
(2, "Few phrases such as yes and thank you"),
(3, "Can answer a few questions"),
(4, "Able to have some basic skills- knows some nouns and verbs"),
(5, "Able to have basic conversation in some concrete areas"),
(6, "Able to have more than basic conversation- knows various tenses, etc."),
(7, "Able to have in depth conversations around daily events"),
(8, "Able to have discussions around abstract concepts"),
(9, "Fluent other than some technical terms"),
(10, "Fluent, including in specialty areas")
        )
    language_skills = models.IntegerField("Language Skills (highest level adult)", blank=True, 
        choices = LANGUAGE_CHOICES)
    employment = models.IntegerField(blank=True)
    finances = models.IntegerField(blank=True)  #family
    transportation = models.IntegerField(blank=True)  #family
    housing = models.IntegerField(blank=True)  #family
    access_to_services = models.IntegerField(blank=True)  #family
    education_or_training = models.IntegerField(blank=True) #School/ Education/ Job Training (parents)
    support_of_children = models.IntegerField(blank=True) #parents
    mental_health = models.IntegerField(blank=True)  #all family members
    social_support = models.IntegerField(blank=True)

    case_summary = models.TextField(max_length=10000, blank = True)
    goals models.TextField(max_length=10000, blank = True) #School/ Education/ Job Training (parents)
