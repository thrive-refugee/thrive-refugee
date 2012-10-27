from esl_manager.models import ESLStudent,  Attended,  Assesment
from django.contrib import admin

class AttendedInline(admin.TabularInline):
    model = Attended
    extra = 1

class AssesmentInline(admin.TabularInline):
    model = Assesment
    extra = 1

class ESLStudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',               {'fields': ['FirstName', 'LastName']}),
        ('Address', {'fields': ['StreetAddress', 'City', 'State', 'Zip']}),
        ('Phones',               {'fields': ['Phones']}),
    ]
    inlines = [AttendedInline, AssesmentInline]
    list_display = ('FirstName', 'LastName', 'StreetAddress', 'Phones')
    list_filter = ['FirstName', 'LastName']
    search_fields = ['FirstName', 'LastName']
    

admin.site.register(ESLStudent,  ESLStudentAdmin)
