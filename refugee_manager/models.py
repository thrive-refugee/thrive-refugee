from django.db import models
from django.contrib.auth.models import User

# https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users
class VolunteerInfo(models.Model):
    user = models.OneToOneField(User)

    phone = models.CharField(max_length=255)

