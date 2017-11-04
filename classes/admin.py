from django.contrib import admin

from classes.models import Attendee
from classes.models import Attendance
from classes.models import Session


class AttendanceInline(admin.TabularInline):
    model = Attendance


class AttendeeAdmin(admin.ModelAdmin):
    pass


class SessionAdmin(admin.ModelAdmin):
    inlines = [
        AttendanceInline,
    ]


admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Session, SessionAdmin)
