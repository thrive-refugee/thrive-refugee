from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars

from .models import Volunteer, Case, Individual


admin.site.disable_action('delete_selected')
class DeleteNotAllowedModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

# Define an inline admin descriptor for Volunteer model
# which acts a bit like a singleton
class VolunteerInlineAdmin(admin.TabularInline):
    model = Volunteer
    can_delete = False


# Define a new User admin
class UserAdminWithVolunteerInfo(UserAdmin):
    inlines = (VolunteerInlineAdmin, )
    list_display = UserAdmin.list_display + ('volunteer_phone_number',)

    def volunteer_phone_number(self, obj):
        return obj.volunteer.phone


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdminWithVolunteerInfo)


class IndividualInlineAdmin(admin.TabularInline):
    model = Individual
    can_delete = False


class CaseAdmin(DeleteNotAllowedModelAdmin):
    # list view stuff
    list_display = ('active', 'name', 'start', 'end', 'arrival', 'origin', 'language', 'family_members')
    def family_members(self, obj):
        individuals = obj.individuals.all()
        return '%s: %s' % (len(individuals),
                           truncatechars(', '.join(i.name for i in individuals), 50))

    list_display_links = list_display
    list_filter = ('active', 'start', 'arrival', 'origin', 'language',)
    search_fields = Case._meta.get_all_field_names()

    # individual stuff
    inlines = (IndividualInlineAdmin,)

admin.site.register(Case, CaseAdmin)


class IndividualAdmin(DeleteNotAllowedModelAdmin):
    # list view stuff
    list_display = Individual._meta.get_all_field_names()
    list_display_links = list_display
    list_filter = ('case', 'date_of_birth', 'case__active')
    search_fields = [f for f in Individual._meta.get_all_field_names()
                     if f != 'case']  # can't search on foriegn keys

    # individual stuff
    #filter_horizontal = ('volunteers',)

admin.site.register(Individual, IndividualAdmin)


