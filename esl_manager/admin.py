from esl_manager.models import ESLStudent,  Attended
from django.contrib import admin

class AttendedInline(admin.TabularInline):
    model = Attended
    extra = 3

class ESLStudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',               {'fields': ['FirstName', 'LastName']}),
        ('Address', {'fields': ['StreetAddress', 'City', 'State', 'Zip'], 'classes': ['collapse']}),
    ]
    inlines = [AttendedInline]
    list_display = ('FirstName', 'LastName', 'StreetAddress')
    list_filter = ['FirstName', 'LastName']
    search_fields = ['FirstName', 'LastName']
    

admin.site.register(ESLStudent,  ESLStudentAdmin)
