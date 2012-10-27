from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Volunteer, Case


# Define an inline admin descriptor for Volunteer model
# which acts a bit like a singleton
class VolunteerInlineAdmin(admin.StackedInline):
    model = Volunteer
    can_delete = False


# Define a new User admin
class UserAdminWithVolunteerInfo(UserAdmin):
    inlines = (VolunteerInlineAdmin, )
    list_display = UserAdmin.list_display + ('volunteer_phone_number',)

    def volunteer_phone_number(self, obj):
        return obj.volunteer.phone


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdminWithVolunteerInfo)


class CaseAdmin(admin.ModelAdmin):
    # list view stuff
    list_display = ('arrival', 'origin', 'employment',)
    list_display_links = list_display
    list_filter = ('arrival', 'origin',)
    search_fields = Case._meta.get_all_field_names()

    # individual stuff
    #filter_horizontal = ('volunteers',)

admin.site.register(Case, CaseAdmin)
