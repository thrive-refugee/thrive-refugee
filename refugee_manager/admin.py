from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars
from django.db.models.fields.related import RelatedField
from django.core.exceptions import FieldError

from .models import Volunteer, Case, Individual, CaseDetail, ActivityNote


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

class CaseDetailInlineAdmin(admin.TabularInline):
    model = CaseDetail
    can_delete = False
    extra = 0

class VolunteerFilter(admin.SimpleListFilter):
    title = 'Volunteer'
    parameter_name = 'volunteer'
    def lookups(self, request, model_admin):
        return [
            (v.id, '%s %s' % (v.user.first_name, v.user.last_name))
            for v in Volunteer.objects.order_by('user__first_name').all()
        ]

    def queryset(self, request, queryset):
        if self.value():
            try:
                # for Cases (many-to-many)
                return queryset.filter(volunteers=self.value())
            except FieldError:
                # for one-to-many where its singular
                return queryset.filter(volunteer=self.value())
        else:
            return queryset

class CaseAdmin(DeleteNotAllowedModelAdmin):
    # list view stuff
    list_display = ('active', 'name', 'start', 'end', 'arrival', 'volunteers_list', 'phone', 'family_members')
    def volunteers_list(self, obj):
        return ', '.join(v.user.first_name + ' ' + v.user.last_name for v in obj.volunteers.all())
    volunteers_list.short_description = 'Volunteers'
    def family_members(self, obj):
        individuals = obj.individuals.all()
        return '%s: %s' % (len(individuals),
                           truncatechars(', '.join(i.name for i in individuals), 50))

    list_display_links = list_display
    list_filter = ('active', VolunteerFilter, 'start', 'arrival', 'origin', 'language',)
    search_fields = [f.name for f in Individual._meta.local_fields if not isinstance(f, RelatedField)]
    ordering = ('-active', 'name',)

    # individual stuff
    inlines = (CaseDetailInlineAdmin, IndividualInlineAdmin,)

admin.site.register(Case, CaseAdmin)


class IndividualAdmin(DeleteNotAllowedModelAdmin):
    # list view stuff
    list_display = ('case_link', 'name', 'relation', 'date_of_birth', )
    def case_link(self, obj):
        case = obj.case
        return '<a href="../../%s/%s/%d">%s</a>' % (
            case._meta.app_label, case._meta.module_name, case.id, unicode(case))
    case_link.allow_tags = True
    case_link.short_description = 'Case'

    list_display_links = ('name', 'relation', 'date_of_birth',)
    list_filter = ('case', 'date_of_birth', 'case__active')
    search_fields = [f.name for f in Individual._meta.local_fields if not isinstance(f, RelatedField)]
    ordering = ('name',)

admin.site.register(Individual, IndividualAdmin)


class ActivityNoteAdmin(DeleteNotAllowedModelAdmin):
    # list view stuff
    list_display = ('case', 'volunteer', 'date', 'description_trunc', 'minutes')
    def description_trunc(self, obj):
        return truncatechars(obj.description, 30)
    description_trunc.short_description = 'Description'
    list_display_links = list_display
    list_filter = ('case', VolunteerFilter, 'date', 'minutes')
    search_fields = ('description',)
    ordering = ('-date',)

admin.site.register(ActivityNote, ActivityNoteAdmin)