from __future__ import absolute_import
from django.contrib import admin
from django.http import HttpResponse
from .models import Donor


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_donation'
    actions_on_bottom = True
    list_display = 'name', 'business', 'last_donation'
    search_fields = 'name', 'business', 'email', 'address'

    def make_list(self, request, queryset):
        response = HttpResponse(content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename=donors.txt'
        for donor in queryset:
            if donor.email:
                response.write("{} <{}>\n".format(donor.name, donor.email))
        return response
    make_list.short_description = "Create mailing list (plain text)"

    actions = [make_list]
