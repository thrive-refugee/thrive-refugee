from django.contrib import admin

from classes.models import Attendee
from classes.models import Attendance
from classes.models import Session
from classes.models import WalkinClass


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1
    verbose_name = 'Attendee'
    verbose_name_plural = 'Attendees'
    fields = ('attendee', 'start_date_time', "stop_date_time", 'notes')


class SessionInline(admin.TabularInline):
    model = Session
    extra = 1
    fields = ('start_date_time', 'stop_date_time', 'teacher')


class AttendeeAdmin(admin.ModelAdmin):
    pass


class SessionAdmin(admin.ModelAdmin):
    inlines = [
        AttendanceInline,
    ]
    fields = ('walk_in_class','teacher', 'start_date_time', "stop_date_time", )
    list_display= ('walk_in_class', 'start_date_time',)

class WalkinClassAdmin(admin.ModelAdmin):
    inlines = [
        SessionInline,
    ]

admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(WalkinClass, WalkinClassAdmin)
