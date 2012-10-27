from django.db import models
from django.contrib.auth.models import User

# https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users
class Volunteer(models.Model):
    user = models.OneToOneField(User)

    phone = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Volunteer Info'
        verbose_name_plural = 'Volunteer Info'

