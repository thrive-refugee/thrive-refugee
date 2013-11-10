from django.contrib import admin
from django.db.models.fields import CharField, TextField

from employment_manager.models import EmploymentClient, Job, Skill, Assesment, Language
from refugee_manager.admin import CaseOrClientAdmin, VolunteerFilter


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


admin.site.register(EmploymentClient, EmploymentClientAdmin)
