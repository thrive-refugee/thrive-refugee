from django.contrib import admin

from .models import EventType


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('label', 'abbr')


admin.site.register(EventType, EventTypeAdmin)
