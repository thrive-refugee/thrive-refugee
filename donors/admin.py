from __future__ import absolute_import
from django.contrib import admin
from .models import Donor


class DonorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Donor, DonorAdmin)
