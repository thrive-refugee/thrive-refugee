from employment_manager.models import EmploymentClient, Job, Skill, Assesment, Language
from django.contrib import admin


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


class EmploymentClientAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['FirstName', 'LastName', 'Active']}),
        ('Address', {'fields': ['StreetAddress', 'City', 'State', 'Zip']}),
        ('Phones', {'fields': ['Phones']}),
    ]
    inlines = [JobInline, SkillInline, AssesmentInline, LanguageInline]
    list_display = ('FirstName', 'LastName', 'StreetAddress', 'Phones')
    list_filter = ['FirstName', 'LastName']
    search_fields = ['FirstName', 'LastName']


admin.site.register(EmploymentClient, EmploymentClientAdmin)
