from __future__ import absolute_import, unicode_literals
from django.db import models
import localflavor.us.models
import datetime


class Donor(models.Model):
    name = models.CharField(max_length=64)
    business = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    phone = localflavor.us.models.PhoneNumberField(null=True, blank=True)
    address = models.TextField(blank=True)
    last_amount = models.DecimalField(max_digits=9+2, decimal_places=2)
    last_donation = models.DateField(default=datetime.date.today)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        if self.business:
            return "{} ({})".format(self.name, self.business)
        else:
            return self.name
