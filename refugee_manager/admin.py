from datetime import datetime, date, timedelta

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars
from django.db.models import Sum, Q, Count
from django.db.models.fields import CharField, TextField
from django.core.exceptions import FieldError
from django import forms

from .models import Volunteer, Case, Individual, CaseDetail, Assessment, ActivityNote, CaseFile


admin.site.disable_action('delete_selected')


class DeleteNotAllowedModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class VolunteerInlineAdminForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = '__all__'
        widgets = {
            'mailing_address': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        }


class VolunteerInlineAdmin(admin.TabularInline):
    model = Volunteer
    form = VolunteerInlineAdminForm
    can_delete = False


# Define a new User admin
class UserAdminWithVolunteerInfo(UserAdmin):
    inlines = (VolunteerInlineAdmin,)
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


class CaseFileInlineAdmin(admin.TabularInline):
    model = CaseFile
    can_delete = True
    extra = 1


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
                (request.user.username, (request.user.first_name + ' ' + request.user.last_name))
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
                (str(c.id), '%s' % (c.name))
                for c in Case.objects.order_by('name').all()
            ]
        else:
            return [
                (str(c.id), '%s' % (c.name))
                for c in Case.objects.order_by('name').filter(volunteers__user__exact=request.user)
            ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(case=self.value())
        else:
            return queryset


def previous_months(curr_month, count):
    for i in range(0, count):
        yield curr_month
        if curr_month.month > 1:
            curr_month = date(curr_month.year, curr_month.month - 1, 1)
        else:
            curr_month = date(curr_month.year - 1, 12, 1)


class CaseOpenDuringRangeStartFilter(admin.SimpleListFilter):
    title = 'Open Cases - From Month'
    parameter_name = 'open_during_start'

    def lookups(self, request, model_admin):
        choices = []
        curr_month = date(date.today().year, date.today().month, 1)
        for month in previous_months(curr_month, 24):
            choices.append((month.isoformat(), month.strftime('%b %Y')))

        return choices

    def queryset(self, request, queryset):
        # case ended after the specified start-date (or no end)
        if self.value():
            return queryset.filter(Q(end__gte=self.value()) | Q(end__isnull=True))
        else:
            return queryset


class CaseOpenDuringRangeEndFilter(admin.SimpleListFilter):
    title = 'Open Cases - Through Month'
    parameter_name = 'open_during_end'

    def lookups(self, request, model_admin):
        choices = []
        curr_month = date(date.today().year, date.today().month, 1)
        for month in previous_months(curr_month, 24):
            if month.month < 12:
                next_month = date(month.year, month.month + 1, 1)
            else:
                next_month = date(month.year + 1, 1, 1)
            end_of_month = next_month - timedelta(days=1)
            choices.append((end_of_month.isoformat(), month.strftime('%b %Y')))

        return choices

    def queryset(self, request, queryset):
        # case started before the specified end-date
        if self.value():
            return queryset.filter(start__lte=self.value())
        else:
            return queryset


class CaseAdminForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'size': 60}),
            'employment': forms.TextInput(attrs={'size': 60}),
            'english_classes': forms.TextInput(attrs={'size': 60}),
            'origin': forms.TextInput(attrs={'size': 60}),
            'language': forms.TextInput(attrs={'size': 60}),
            'green_card': forms.TextInput(attrs={'size': 60}),
            'dhs_worker': forms.TextInput(attrs={'size': 60}),
            'school': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
            'doctor': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
            'other1': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
            'other2': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
            'other3': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
            'other4': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
            'other5': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
        }


class CaseOrClientAdmin(DeleteNotAllowedModelAdmin):
    '''
    Common functionality for EmploymentClients and refugee Cases which both have volunteer relations & security
    '''

    def volunteers_list(self, obj):
        return ', '.join(v.user.first_name + ' ' + v.user.last_name if v.user.first_name + v.user.last_name.strip() != "" else v.user.username for v in obj.volunteers.all())
    volunteers_list.short_description = 'Volunteers'

    def get_queryset(self, request):
        qs = super(CaseOrClientAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return self.order_qs(qs).filter(volunteers__user__exact=request.user)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'volunteers':
            if request.user.is_superuser:
                kwargs['queryset'] = Volunteer.objects
            else:
                kwargs['queryset'] = Volunteer.objects.filter(user=request.user)
        return super(CaseOrClientAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


def filter_key_to_name(filters, key):
    """
    :param filters: a ModelAdmin's list_filter
    :param key: a string from a URL
    :return: the nice name for the filter
    """
    for filter in filters:
        if getattr(filter, 'parameter_name', None) == key:
            # a SimpleListFilter class
            return filter.title
    return key.replace('__', ' ').replace('exact','')


class CaseTotallingChangeList(ChangeList):
    def get_results(self, *args, **kwargs):
        super(CaseTotallingChangeList, self).get_results(*args, **kwargs)

        q = self.result_list.aggregate(total_cases=Count('id'))
        self.total_cases = q['total_cases']

        q = self.result_list.aggregate(total_individuals=Count('individuals'))
        self.total_individuals = q['total_individuals']

        request = args[0]
        self.active_filters = {filter_key_to_name(CaseAdmin.list_filter, filter_key): value
                               for filter_key, value
                               in request.GET.iteritems()}


class CaseAdmin(CaseOrClientAdmin):
    form = CaseAdminForm

    # list view stuff
    list_display = (
        'active', 'name', 'start', 'end', 'arrival', 'volunteers_list', 'phone',
        'family_members', 'next_assessment')

    def family_members(self, obj):
        individuals = obj.individuals.all()
        return '%s: %s' % (len(individuals),
                           truncatechars(', '.join(i.name for i in individuals), 50))

    def next_assessment(self, obj):
        ONEMONTH = timedelta(days=30)
        SIXMONTHS = timedelta(days=183)
        oas = obj.assessment
        count = oas.count()
        if count == 0:
            # Schedule 1mo from start
            return obj.start + ONEMONTH
        else:
            # Every six months from start
            last = oas.latest()
            timepassed = last.date - obj.start
            chunks = timepassed.days / SIXMONTHS.days  # GRR timedelta doesn't support division
            return obj.start + (int(chunks) + 1) * SIXMONTHS

    list_display_links = list_display
    list_filter = ('active', VolunteerFilter, 'start', 'arrival', 'origin', 'language',
                   CaseOpenDuringRangeStartFilter, CaseOpenDuringRangeEndFilter,)
    search_fields = [f.name for f in Case._meta.local_fields if isinstance(f, (CharField, TextField))]
    ordering = ('-active', 'name',)

    # individual stuff
    inlines = (CaseDetailInlineAdmin, IndividualInlineAdmin, CaseFileInlineAdmin)

    def order_qs(self, qs):
        return qs.order_by('name')

    change_list_template = 'refugee_manager/case_admin_list.html'

    def get_changelist(self, request):
        return CaseTotallingChangeList

admin.site.register(Case, CaseAdmin)


class IndividualAdmin(DeleteNotAllowedModelAdmin):
    # list view stuff
    list_display = ('case_link', 'name', 'relation', 'date_of_birth',)

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

    def get_queryset(self, request):
        qs = super(IndividualAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.order_by('case').filter(case__volunteers__user__exact=request.user)
    list_display_links = ('name', 'relation', 'date_of_birth',)
    list_filter = ('case', 'date_of_birth', 'case__active')
    search_fields = [f.name for f in Individual._meta.local_fields if isinstance(f, (CharField, TextField))]
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

    def get_queryset(self, request):
        qs = super(AssesmentAdmin, self).get_queryset(request)
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
            except (ValueError, TypeError):
                continue

            total += value
            denom += 10 if value != 0 else 0
        if denom == 0:
            return u"0/0 , 0%"
        return "{:.0f}/{:.0f}  <strong><span style=font-size:130%;>{:.0f}%</span></strong>".format(total, denom, (total / denom) * 100)
    calc_score.allow_tags = True
    calc_score.description = "Score"
    list_filter = ('date', 'case')

admin.site.register(Assessment, AssesmentAdmin)


class MinuteTotallingChangeList(ChangeList):
    def get_results(self, *args, **kwargs):
        super(MinuteTotallingChangeList, self).get_results(*args, **kwargs)
        q = self.result_list.aggregate(minutes_total=Sum('minutes'))
        total = q['minutes_total'] or 0
        self.total_hours = total / 60
        self.total_minutes = total % 60


class ActivityNoteAdmin(DeleteNotAllowedModelAdmin):
    # list view stuff
    list_display = ('case', 'volunteer', 'date', 'description_trunc', 'minutes')

    def description_trunc(self, obj):
        return truncatechars(obj.description, 30)

    def get_queryset(self, request):
        qs = super(ActivityNoteAdmin, self).get_queryset(request)
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

    change_list_template = 'refugee_manager/activitynote_admin_list.html'

    def get_changelist(self, request):
        return MinuteTotallingChangeList

    description_trunc.short_description = 'Description'
    list_display_links = list_display
    list_filter = (CaseFilter, VolunteerFilter, 'date')
    date_hierarchy = 'date'
    search_fields = ('description',)
    ordering = ('-date',)

admin.site.register(ActivityNote, ActivityNoteAdmin)


# class EventAdmin(admin.ModelAdmin):
#    # list view stuff
#    list_display = ('case', 'volunteer', 'start', 'end', 'title_trunc')
#
#    def title_trunc(self, obj):
#        return truncatechars(obj.title, 30)
#    title_trunc.short_description = 'Title'
#
#    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#        if db_field.name == 'case':
#            if request.user.is_superuser:
#                kwargs['queryset'] = Case.objects.order_by('name')
#            else:
#                kwargs['queryset'] = Case.objects.order_by('name').filter(volunteers__user=request.user)
#
#        if db_field.name == 'volunteer':
#            if request.user.is_superuser:
#                kwargs['queryset'] = Volunteer.objects
#            else:
#                kwargs['queryset'] = Volunteer.objects.filter(user=request.user)
#        return super(EventAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
#
#    def queryset(self, request):
#        qs = super(EventAdmin, self).queryset(request)
#        if request.user.is_superuser:
#            return qs.order_by('case')
#        return qs.order_by('case').filter(volunteer__user__exact=request.user)
#
#    list_display_links = list_display
#    list_filter = (CaseFilter, VolunteerFilter, 'start')
#    date_hierarchy = 'start'
#    search_fields = [f.name for f in Event._meta.local_fields if isinstance(f, (CharField, TextField))]
#    ordering = ('-start',)
#
# admin.site.register(Event, EventAdmin)
