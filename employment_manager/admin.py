from django.contrib import admin
from django.db.models.fields import CharField, TextField
from django.template.defaultfilters import truncatechars

from employment_manager.models import EmploymentClient, Job, Skill, Assesment, Language, ActivityNote
from refugee_manager.admin import CaseOrClientAdmin, VolunteerFilter, DeleteNotAllowedModelAdmin, MinuteTotallingChangeList
from refugee_manager.models import Volunteer


class JobInline(admin.TabularInline):
    model = Job
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class AssesmentInline(admin.TabularInline):
    model = Assesment
    extra = 1


class LanguageInline(admin.TabularInline):
    model = Language
    extra = 1


class EmploymentClientAdmin(CaseOrClientAdmin):
    fieldsets = [
        ('Volunteers', {'fields': ['volunteers']}),
        ('Name', {'fields': ['FirstName', 'LastName', 'Active']}),
        ('Address', {'fields': ['StreetAddress', 'City', 'State', 'Zip']}),
        ('Phones', {'fields': ['Phones']}),
        ('Other', {'fields': ['Other']}),
    ]
    inlines = [JobInline, SkillInline, AssesmentInline, LanguageInline]
    list_display = ('Active', 'FirstName', 'LastName', 'StreetAddress', 'Phones', 'volunteers_list')
    list_display_links = list_display
    list_filter = ['Active', VolunteerFilter, 'FirstName', 'LastName']
    search_fields = [f.name for f in EmploymentClient._meta.local_fields if isinstance(f, (CharField, TextField))]
    ordering = ('-Active', 'LastName', 'FirstName')

    def volunteers_list(self, obj):
        return ', '.join(v.user.first_name + ' ' + v.user.last_name if v.user.first_name + v.user.last_name.strip() != "" else v.user.username for v in obj.volunteers.all())
    volunteers_list.short_description = 'Volunteers'

    def order_qs(self, qs):
        return qs.order_by('LastName').order_by('FirstName')

admin.site.register(EmploymentClient, EmploymentClientAdmin)


class EmploymentClientFilter(admin.SimpleListFilter):
    title = 'Employment Client'
    parameter_name = 'employment_client'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return [
                (str(c.id), '%s' % (str(c)))
                for c in EmploymentClient.objects.order_by('LastName', 'FirstName').all()
            ]
        else:
            return [
                (str(c.id), '%s' % (str(c)))
                for c in EmploymentClient.objects.order_by('LastName', 'FirstName').filter(volunteers__user__exact=request.user)
            ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(employment_client=self.value())
        else:
            return queryset


class ActivityNoteAdmin(DeleteNotAllowedModelAdmin):
    # list view stuff
    list_display = ('employment_client', 'volunteer', 'date', 'description_trunc', 'minutes')

    def description_trunc(self, obj):
        return truncatechars(obj.description, 30)

    def get_queryset(self, request):
        qs = super(ActivityNoteAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.order_by('employment_client')
        return qs.order_by('employment_client').filter(volunteer__user__exact=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'employment_client':
            if request.user.is_superuser:
                kwargs['queryset'] = EmploymentClient.objects.order_by('LastName', 'FirstName')
            else:
                kwargs['queryset'] = EmploymentClient.objects.order_by('LastName', 'FirstName').filter(volunteers__user=request.user)

        if db_field.name == 'volunteer':
            if request.user.is_superuser:
                kwargs['queryset'] = Volunteer.objects
            else:
                kwargs['queryset'] = Volunteer.objects.filter(user=request.user)
        return super(ActivityNoteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    change_list_template = 'refugee_manager/activitynote_admin_list.html'

    def get_changelist(self, request):
        return MinuteTotallingChangeList

    description_trunc.short_description = 'Description'
    list_display_links = list_display
    list_filter = (EmploymentClientFilter, VolunteerFilter, 'date')
    date_hierarchy = 'date'
    search_fields = ('description',)
    ordering = ('-date',)

admin.site.register(ActivityNote, ActivityNoteAdmin)
