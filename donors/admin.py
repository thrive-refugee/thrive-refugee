from __future__ import absolute_import
import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import Donor, Donation


class DonationInline(admin.TabularInline):
    model = Donation
    extra = 0


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    inlines = [
        DonationInline
    ]
    # date_hierarchy = 'last_donation'
    actions_on_bottom = True
    list_display = 'name', 'business', 'last_donation', 'last_amount'
    search_fields = 'name', 'business', 'email', 'address'

    @staticmethod
    def last_donation(obj):
        return obj.donation_set.latest().when

    @staticmethod
    def last_amount(obj):
        return obj.donation_set.latest().amount

    actions = []

    def make_list(self, request, queryset):
        response = HttpResponse(content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename=donors.txt'
        for donor in queryset:
            if donor.email:
                response.write("{} <{}>\n".format(donor.name, donor.email))
        return response
    make_list.short_description = "Create email list (plain text)"
    actions.append(make_list)

    def make_csv(self, request, queryset):
        fields = ('name', 'business', 'email', 'phone', 'address', 'last_donation', 'notes')
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=donors.csv'
        writer = csv.DictWriter(response, fields, extrasaction='ignore')
        writer.writeheader()
        for donor in queryset:
            row = {"last_donation": self.last_donation(donor)}
            row.update(vars(donor))
            writer.writerow(row)
        return response
    make_csv.short_description = "Create CSV"
    actions.append(make_csv)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    date_hierarchy = 'when'
    actions_on_bottom = True
    list_display = 'donor', 'when', 'amount', 'memo'
    search_fields = 'donor', 'memo'

    actions = []

    def make_csv(self, request, queryset):
        fields = ('name', 'business', 'when', 'amount', 'memo')
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=donations.csv'
        writer = csv.DictWriter(response, fields, extrasaction='ignore')
        writer.writeheader()
        for donation in queryset:
            row = {
                "name": donation.donor.name,
                "business": donation.donor.business,
            }
            row.update(vars(donation))
            writer.writerow(row)
        return response
    make_csv.short_description = "Create CSV"
    actions.append(make_csv)
