from django.contrib.contenttypes import generic
from django.contrib import admin

from .models import Event
from .models import EventType
from .models import Note
from .models import Occurrence


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('label', 'abbr')


class NoteAdmin(admin.ModelAdmin):
    list_display = ('note', 'created')
    pass


class OccurrenceInline(admin.TabularInline):
    model = Occurrence
    extra = 1


class EventNoteInline(generic.GenericTabularInline):
    model = Note
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'for_case', 'event_type', 'description')
    list_filter = ('for_case', 'event_type',)
    search_fields = ('title', 'description')
    inlines = [EventNoteInline, OccurrenceInline]
    pass

admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Note, NoteAdmin)
