from django.conf.urls import url
from swingtime import views

urlpatterns = [

    '',

    url(
        r'^(?:calendar/)?$',
        views.calendar_view,
        name='swingtime-calendar'
    ),

    url(
        r'^events/add/$',
        views.add_event,
        name='swingtime-add-event'
    ),

    url(
        r'^events/(\d+)/$',
        views.event_view,
        name='swingtime-event'
    ),

    url(
        r'^events/(\d+)/(\d+)/$',
        views.occurrence_view,
        name='swingtime-occurrence'
    ),

    url(r'^ics/(?P<slug>.*)$', views.ics_feed, name='swingtime-ical'),

    url(r'^json$', views.json_feed, name='swingtime-json'),

]
