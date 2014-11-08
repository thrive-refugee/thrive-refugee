from django.db import models
import datetime


class Donor(models.Model):
    name = models.CharField()
    business = models.CharField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=10+3)  # django.contrib.localflavor.us.forms.USPhoneNumberField
    address = models.TextField(blank=True)
    last_amount = models.DecimalField(decimal_places=2)
    last_donation = models.DateField(default=datetime.date.today)
    notes = models.TextField(blank=True)
