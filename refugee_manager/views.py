# Create your views here.
import datetime

from django.http import HttpResponse, Http404
from django.core import serializers
from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.urlresolvers import reverse

from simple_rest import Resource
from django_ical.views import ICalFeed

# from .models import Event, Calendar


# @admin_required
# class Events(Resource):
#
#    def get(self, request, event_id=None, **kwargs):
#        json_serializer = serializers.get_serializer('json')()
#        if event_id:
#            events = json_serializer.serialize(Event.objects.filter(pk=event_id))
#        else:
#            events = json_serializer.serialize(Event.objects.all())
#        return HttpResponse(events, content_type='application/json', status=200)
#
#    def post(self, request, *args, **kwargs):
#        Event.objects.create(
#            case=1,
#            volunteer=1,
#            start=request.POST.get('start'),
#            end=request.POST.get('end'),
#            allDay=request.POST.get('allDay'),
#            title=request.POST.get('title'),
#            description=request.POST.get('description')
#        )
#        return HttpResponse(status=201)
#
#    def delete(self, request, event_id):
#        event = Event.objects.get(pk=event_id)
#        event.delete()
#        return HttpResponse(status=200)
#
#
# def showCalendar(request):
#    context = {}
#    return render(request, 'refugee_manager/calendar.html', context)
#
#
# class EventFeed(ICalFeed):
#    """
#    A simple event calender
#
#    http://django-ics.readthedocs.org/en/latest/usage.html
#    """
#    product_id = '-//refugeesupportgr.com//Global//EN'
#    timezone = 'US/Detroit'
#    title = 'Thrive: All Events'
#    description = 'All Thrive events'
#
#    def __init__(self, request, slug):
#        super(EventFeed, self).__init__()
#        self.request = request
#        self.slug = slug
#        try:
#            self.calendar = Calendar.objects.get(slug=slug)
#        except Calendar.DoesNotExist:
#            raise Http404
#
#        if not self.calendar.volunteer.user.is_active:
#            raise ValueError("Inactive User")
#
#        if self.calendar.everything and not self.calendar.volunteer.user.is_superuser:
#            raise ValueError("Not Superuser")
#
#    def items(self):
#        if self.calendar.everything:
#            rv = Event.objects.all()
#        else:
#            rv = Event.objects.filter(case__volunteers=self.calendar.volunteer)
#
#        return rv.filter(end__gte=datetime.datetime.today()).order_by('-start')
#
#    def item_title(self, item):
#        return "{}: {}".format(item.case.name, item.title)
#
#    def item_description(self, item):
#        return item.description
#
#    def item_start_datetime(self, item):
#        return item.start
#
#    def item_end_datetime(self, item):
#        return item.end
#
#    def item_link(self, item):
#        return self.request.build_absolute_uri("/admin/refugee_manager/event/{}".format(item.id))
#
#    def item_guid(self, item):
#        return 'event:{}@refugeesupportgr.com'.format(item.id)


def ics_feed(*p, **kw):
    return EventFeed(*p, **kw)(*p, **kw)
