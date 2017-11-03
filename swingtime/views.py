import calendar
import json
from datetime import datetime, timedelta
import time as time_mod
import logging

from django import http
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from swingtime.models import Event, Occurrence, ICal_Calendar
from swingtime import utils, forms
from swingtime.conf import settings as swingtime_settings

from dateutil import parser

if swingtime_settings.CALENDAR_FIRST_WEEKDAY is not None:
    calendar.setfirstweekday(swingtime_settings.CALENDAR_FIRST_WEEKDAY)


@login_required()
def event_view(
    request,
    pk,
    template='swingtime/event_detail.html',
    event_form_class=forms.EventForm,
    recurrence_form_class=forms.MultipleOccurrenceForm
):
    '''
    View an ``Event`` instance and optionally update either the event or its
    occurrences.

    Context parameters:

    event
        the event keyed by ``pk``

    event_form
        a form object for updating the event

    recurrence_form
        a form object for adding occurrences
    '''
    event = get_object_or_404(Event, pk=pk)

    if not request.user.is_superuser:
        if request.user.volunteer not in event.case.volunteers.all():
            raise http.Http404

    event_form = recurrence_form = None
    if request.method == 'POST':
        if '_update' in request.POST:
            event_form = event_form_class(request.POST, instance=event, request=request)
            if event_form.is_valid():
                event_form.save(event)
                messages.add_message(request, messages.INFO, 'Event updated.')
                return http.HttpResponseRedirect(request.path)
        elif '_add' in request.POST:
            recurrence_form = recurrence_form_class(request.POST)
            if recurrence_form.is_valid():
                recurrence_form.save(event)
                messages.add_message(request, messages.INFO, 'Occurrences added.')
                return http.HttpResponseRedirect(request.path)
        elif '_delete' in request.POST:
            event.delete()
            messages.add_message(request, messages.INFO, 'Event deleted.')
            return http.HttpResponseRedirect('/calendar/')
        else:
            return http.HttpResponseBadRequest('Bad Request')

    data = {
        'event': event,
        'event_form': event_form or event_form_class(instance=event, request=request),
        'recurrence_form': recurrence_form or recurrence_form_class(initial={'dtstart': datetime.now()})
    }
    return render(request, template, data)


@login_required()
def occurrence_view(
    request,
    event_pk,
    pk,
    template='swingtime/occurrence_detail.html',
    form_class=forms.SingleOccurrenceForm
):
    '''
    View a specific occurrence and optionally handle any updates.

    Context parameters:

    occurrence
        the occurrence object keyed by ``pk``

    form
        a form object for updating the occurrence
    '''
    occurrence = get_object_or_404(Occurrence, pk=pk, event__pk=event_pk)

    if not request.user.is_superuser:
        if request.user.volunteer not in occurrence.event.case.volunteers.all():
            raise http.Http404

    if request.method == 'POST':
        if '_delete' in request.POST:
            occurrence.delete()
            messages.add_message(request, messages.INFO, 'Occurrence deleted.')
            return http.HttpResponseRedirect(occurrence.event.get_absolute_url())
        else:
            form = form_class(request.POST, instance=occurrence)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO, 'Occurrence updated.')
                return http.HttpResponseRedirect(request.path)
    else:
        form = form_class(instance=occurrence)

    return render(request, template, {'occurrence': occurrence, 'form': form})


@login_required()
def add_event(
    request,
    template='swingtime/add_event.html',
    event_form_class=forms.EventForm,
    recurrence_form_class=forms.MultipleOccurrenceForm
):
    '''
    Add a new ``Event`` instance and 1 or more associated ``Occurrence``s.

    Context parameters:

    dtstart
        a datetime.datetime object representing the GET request value if present,
        otherwise None

    event_form
        a form object for updating the event

    recurrence_form
        a form object for adding occurrences

    '''
    dtstart = None
    if request.method == 'POST':
        event_form = event_form_class(request.POST, request=request)
        recurrence_form = recurrence_form_class(request.POST)
        if event_form.is_valid() and recurrence_form.is_valid():
            event = event_form.save()
            recurrence_form.save(event)
            messages.add_message(request, messages.INFO, 'Event added.')
            return http.HttpResponseRedirect(event.get_absolute_url())

    else:
        if 'dtstart' in request.GET:
            try:
                dtstart = parser.parse(request.GET['dtstart'])
            except (TypeError, ValueError) as exc:
                # A badly formatted date was found and passed to add_event
                logging.warning(exc)

        dtstart = dtstart or datetime.now()
        event_form = event_form_class(request=request)
        recurrence_form = recurrence_form_class(initial={'dtstart': dtstart})

    return render(
        request,
        template,
        {'dtstart': dtstart, 'event_form': event_form, 'recurrence_form': recurrence_form}
    )


def _datetime_view(
    request,
    template,
    dt,
    timeslot_factory=None,
    items=None,
    params=None
):
    '''
    Build a time slot grid representation for the given datetime ``dt``. See
    utils.create_timeslot_table documentation for items and params.

    Context parameters:

    day
        the specified datetime value (dt)

    next_day
        day + 1 day

    prev_day
        day - 1 day

    timeslots
        time slot grid of (time, cells) rows

    '''
    timeslot_factory = timeslot_factory or utils.create_timeslot_table
    params = params or {}

    return render(request, template, {
        'day': dt,
        'next_day': dt + timedelta(days=+1),
        'prev_day': dt + timedelta(days=-1),
        'timeslots': timeslot_factory(request, dt, items, **params)
    })


@login_required()
def calendar_view(
    request,
    template='swingtime/calendar_view.html',
    queryset=None
):
    data = {
    }
    return render(request, template, data)


from django_ical.views import ICalFeed


class SwingtimeICalFeed(ICalFeed):

    """
    A simple event calender

    http://django-ics.readthedocs.org/en/latest/usage.html
    """
    # Calendar user agents:
    # * iOS/7.0.3 (11B511) dataaccessd/1.0
    # * Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)

    product_id = '-//refugeesupportgr.com//Everything//EN'
    timezone = settings.TIME_ZONE
    title = 'Thrive: All Events'

    def __init__(self, request, slug):
        super(SwingtimeICalFeed, self).__init__()
        self.request = request
        self.slug = slug
        try:
            self.calendar = ICal_Calendar.objects.get(slug=slug)
        except ICal_Calendar.DoesNotExist:
            raise http.Http404

        if not self.calendar.volunteer.user.is_active:
            raise ValueError("Inactive User")

        if self.calendar.everything and not self.calendar.volunteer.user.is_superuser:
            raise ValueError("Not Superuser")

        if not self.calendar.everything:
            self.title = 'Thrive: ' + self.calendar.volunteer.user.get_full_name()
            self.product_id = '-//refugeesupportgr.com//User:{}//EN'.format(self.calendar.volunteer.user.id)

    def items(self):
        rv = Occurrence.objects.for_user(self.calendar.volunteer.user)
        return rv.filter(end_time__gte=datetime.today()).order_by('-start_time')

    def item_title(self, item):
        if item.event.case:
            return "{}: {}".format(item.event.case, item.event.title)
        else:
            return item.event.title

    def item_description(self, item):
        rv = item.event.description

        if 'google' in self.request.META.get('HTTP_USER_AGENT', '').lower():
            rv += '\n\n' + self.item_link(item)

        return rv

    def item_start_datetime(self, item):
        return item.start_time

    def item_end_datetime(self, item):
        return item.end_time

    def item_link(self, item):
        return reverse('swingtime-event', args=(item.event.id,))

    def item_guid(self, item):
        return 'swingtime:occurance:{}@refugeesupportgr.com'.format(item.id)

    def item_location(self, item):
        return item.address


def ics_feed(*p, **kw):
    return SwingtimeICalFeed(*p, **kw)(*p, **kw)


@login_required()
def json_feed(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    qs = Occurrence.objects.all()
    if not request.user.is_superuser:
        qs = qs.for_user(request.user)
    else:
        pass
    if start:
        qs = qs.filter(end_time__gte=datetime.fromtimestamp(int(start)))
    if end:
        qs = qs.filter(start_time__lte=datetime.fromtimestamp(int(end)))

    response_data = [
        {
            'id': occ.id,
            'title': (
                "{}: {}".format(occ.event.case, occ.event.title)
                if occ.event.case else
                occ.event.title
            ),
            'start': time_mod.mktime(occ.start_time.timetuple()),
            'end': time_mod.mktime(occ.end_time.timetuple()),
            'url': reverse('swingtime-event', args=(occ.event.id,)),
            'allDay': False,
            'className': [
                type(occ.event.case).__name__,
                'color-{}'.format(occ.event.id % 8),
            ],
            'case': {
                'id': occ.event.case.id,
                'type': type(occ.event.case).__name__,
                'title': str(occ.event.case),
            } if occ.event.case else None,
        }
        for occ in qs
    ]

    return http.HttpResponse(json.dumps(response_data), content_type="application/json")
