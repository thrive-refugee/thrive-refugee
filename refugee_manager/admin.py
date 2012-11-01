from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars
from django.db.models.fields.related import RelatedField
from django.core.exceptions import FieldError

from .models import Volunteer, Case, Individual, CaseDetail, Assessment, ActivityNote, Event



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
        if request.user.is_superuser:
            return [
                (v.user.username, '%s %s' % (v.user.first_name, v.user.last_name))
                for v in Volunteer.objects.order_by('user__first_name').all()
            ]
        else:
            return [
                (request.user.username,(request.user.first_name + ' ' + request.user.last_name))
            ]

    def queryset(self, request, queryset):
        if self.value():
            try:
                # for Cases (many-to-many)
                return queryset.filter(volunteers__user__username=self.value())
            except FieldError:
                # for one-to-many where its singular
                return queryset.filter(volunteer__user__username=self.value())
        else:
            return queryset

class CaseFilter(admin.SimpleListFilter):
    title = 'Case'
    parameter_name = 'case'
    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return [
                (c.id, '%s' % (c.name))
                for c in Case.objects.order_by('name').all()
            ]
        else:
            return [
                (c.id, '%s' % (c.name))
                for c in Case.objects.order_by('name').filter(volunteers__user__exact=request.user)
            ]

    def queryset(self, request, queryset):
        if request.user.is_superuser:
            return queryset
        return queryset.order_by('name').filter(volunteer__user__exact=request.user)


class CaseAdmin(DeleteNotAllowedModelAdmin):
    # list view stuff
    list_display = ('active', 'name', 'start', 'end', 'arrival', 'volunteers_list', 'phone', 'family_members')
    def volunteers_list(self, obj):
        return ', '.join(v.user.first_name + ' ' + v.user.last_name if v.user.first_name+v.user.last_name.strip() != "" else v.user.username for v in obj.volunteers.all() )
    volunteers_list.short_description = 'Volunteers'
    def family_members(self, obj):
        individuals = obj.individuals.all()
        return '%s: %s' % (len(individuals),
                           truncatechars(', '.join(i.name for i in individuals), 50))
    def queryset(self, request):
        qs = super(CaseAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.order_by('name').filter(volunteers__user__exact=request.user)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'volunteers':
            if request.user.is_superuser:
                kwargs['queryset'] = Volunteer.objects
            else:
                kwargs['queryset'] = Volunteer.objects.filter(user=request.user)
        return super(CaseAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    list_display_links = list_display
    list_filter = ('active', VolunteerFilter, 'start', 'arrival', 'origin', 'language',)
    search_fields = [f.name for f in Case._meta.local_fields if not isinstance(f, RelatedField)]
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'case':
            if request.user.is_superuser:
                kwargs['queryset'] = Case.objects.order_by('name')
            else:
                kwargs['queryset'] = Case.objects.order_by('name').filter(volunteers__user=request.user)

        return super(IndividualAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        qs = super(IndividualAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.order_by('case').filter(case__volunteers__user__exact=request.user)
    list_display_links = ('name', 'relation', 'date_of_birth',)
    list_filter = ('case', 'date_of_birth', 'case__active')
    search_fields = [f.name for f in Individual._meta.local_fields if not isinstance(f, RelatedField)]
    ordering = ('name',)

admin.site.register(Individual, IndividualAdmin)

class AssesmentAdmin(admin.ModelAdmin):
    list_display = ('case_link', 'date', 'calc_score')
    def case_link(self, obj):
        case = obj.case
        return '<a href="../../%s/%s/%d">%s</a>' % (
            obj._meta.app_label, obj._meta.module_name, obj.id, unicode(case))
    case_link.allow_tags = True
    case_link.short_description = 'Assessment'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'case':
            if request.user.is_superuser:
                kwargs['queryset'] = Case.objects.order_by('name')
            else:
                kwargs['queryset'] = Case.objects.order_by('name').filter(volunteers__user=request.user)
        
        return super(AssesmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        
    def queryset(self, request):
        qs = super(AssesmentAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.order_by('case').filter(case__volunteers__user__exact=request.user)    
		
    def calc_score(self, obj):
        total = 0.0
        denom = 0.0
        q = obj.get_fields()[3:]
        # return unicode(q)
        for value in q:
            try:
                value = int(value[1])
                # return unicode(value)
            except:
                continue

            total += value
            denom += 10 if value != 0 else 0
        if denom == 0: return u"0/0 , 0%"
        return "{:.0f}/{:.0f}  <strong><span style=font-size:130%;>{:.0f}%</span></strong>".format(total, denom, (total/denom)*100)
    calc_score.allow_tags = True
    calc_score.description = "Score"
    list_filter = ('date','case')

admin.site.register(Assessment, AssesmentAdmin)


class ActivityNoteAdmin(DeleteNotAllowedModelAdmin):
    # list view stuff
    list_display = ('case', 'volunteer', 'date', 'description_trunc', 'minutes')
    def description_trunc(self, obj):
        return truncatechars(obj.description, 30)

    def queryset(self, request):
        qs = super(ActivityNoteAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs.order_by('case')
        return qs.order_by('case').filter(volunteer__user__exact=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'case':
            if request.user.is_superuser:
                kwargs['queryset'] = Case.objects.order_by('name')
            else:
                kwargs['queryset'] = Case.objects.order_by('name').filter(volunteers__user=request.user)

        if db_field.name == 'volunteer':
            if request.user.is_superuser:
                kwargs['queryset'] = Volunteer.objects
            else:
                kwargs['queryset'] = Volunteer.objects.filter(user=request.user)
        return super(ActivityNoteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


    description_trunc.short_description = 'Description'
    list_display_links = list_display
    list_filter = (CaseFilter, VolunteerFilter, 'date')
    date_hierarchy = 'date'
    search_fields = ('description',)
    ordering = ('-date',)

admin.site.register(ActivityNote, ActivityNoteAdmin)

class EventAdmin(admin.ModelAdmin):
    # list view stuff
    list_display = ('case', 'volunteer', 'start', 'end', 'title_trunc')
    def title_trunc(self, obj):
        return truncatechars(obj.title, 30)
    title_trunc.short_description = 'Title'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'case':
            if request.user.is_superuser:
                kwargs['queryset'] = Case.objects.order_by('name')
            else:
                kwargs['queryset'] = Case.objects.order_by('name').filter(volunteers__user=request.user)

        if db_field.name == 'volunteer':
            if request.user.is_superuser:
                kwargs['queryset'] = Volunteer.objects
            else:
                kwargs['queryset'] = Volunteer.objects.filter(user=request.user)
        return super(EventAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        qs = super(EventAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs.order_by('case')
        return qs.order_by('case').filter(volunteer__user__exact=request.user)

    list_display_links = list_display
    list_filter = (CaseFilter, VolunteerFilter, 'start')
    date_hierarchy = 'start'
    search_fields = ('description',)
    ordering = ('-start',)

admin.site.register(Event, EventAdmin)

