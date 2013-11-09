from django.conf.urls import patterns, include, url

#from .views import Events
#from .views import showCalendar
from .views import ics_feed


urlpatterns = patterns(
    '',
    # Allow access to the events resource collection
    #url(r'^events/?$', Events.as_view()),

    # Allow access to a single event resource
    #url(r'^events/(?P<event_id>[0-9]+)/?$', Events.as_view()),

    # calendar base page
    #url(r'^calendar/?$', showCalendar),
    url(r'^ics/(?P<slug>.*)$', ics_feed),

)
