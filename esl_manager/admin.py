from esl_manager.models import ESLStudent,  Attended
from django.contrib import admin

class AttendedInline(admin.TabularInline):
    model = Attended
    extra = 3

class ESLStudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',               {'fields': ['FirstName', 'LastName']}),
        ('Address', {'fields': ['StreetAddress', 'City', 'State', 'Zip']}),
        ('Phones',               {'fields': ['Phones']}),
    ]
    inlines = [AttendedInline]
    list_display = ('FirstName', 'LastName', 'StreetAddress', 'Phones')
    list_filter = ['FirstName', 'LastName']
    search_fields = ['FirstName', 'LastName']
    

admin.site.register(ESLStudent,  ESLStudentAdmin)
