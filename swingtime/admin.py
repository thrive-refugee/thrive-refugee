from django.contrib.contenttypes import generic
from django.contrib import admin

from .models import Event
from .models import EventType
from .models import Note
from .models import Occurrence

from refugee_manager.models import Case


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


# Hidden because we're using the swingtime form
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'for_case', 'event_type', 'description')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'for_case':
            if request.user.is_superuser:
                kwargs['queryset'] = Case.objects.order_by('name')
            else:
                kwargs['queryset'] = Case.objects.order_by('name').filter(volunteers__user=request.user)
        return super(EventAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        qs = super(EventAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(for_case__volunteers__user__exact=request.user)
    
    list_filter = ('for_case', 'event_type',)
    search_fields = ('title', 'description')
    inlines = [EventNoteInline, OccurrenceInline]

admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Note, NoteAdmin)
