from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Volunteer


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
