from django.db import models


class IntegerRangeField(models.IntegerField):

    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class EmploymentClient(models.Model):
    FirstName = models.CharField("First Name", max_length=50)
    LastName = models.CharField("Last Name", max_length=80)
    StreetAddress = models.CharField("Address", max_length=50)
    City = models.CharField(max_length=20)
    State = models.CharField(max_length=2)
    Zip = models.CharField(max_length=10)
    Phones = models.CharField(max_length=50, blank=True)
    Active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Employment Client'
        verbose_name_plural = 'Employment Clients'

    def __unicode__(self):
        return self.FirstName


class Job(models.Model):
    employment_client = models.ForeignKey(EmploymentClient)
    Company = models.CharField("Company", max_length=50)
    Title = models.CharField("Title", max_length=80)
    Description = models.CharField('Description', max_length=200, blank=True)
    StartDate = models.DateField('Start Date')
    EndDate = models.DateField('End Date')


class Skill(models.Model):
    employment_client = models.ForeignKey(EmploymentClient)
    Description = models.CharField("Description", max_length=200)


class Assesment(models.Model):
    employment_client = models.ForeignKey(EmploymentClient)
    Name = models.CharField("Name", max_length=20, blank=True)
    TakenDate = models.DateField('Taken')
    Score = models.IntegerField()


class Language(models.Model):
    employment_client = models.ForeignKey(EmploymentClient)
    Name = models.CharField("Language", max_length=20)
    # http://en.wikipedia.org/wiki/ILR_scale
    Scale = IntegerRangeField("ILR Scale", min_value=1, max_value=5)
