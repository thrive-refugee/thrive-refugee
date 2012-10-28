# Create your views here.

from django.http import HttpResponse
from django.core import serializers

from simple_rest import Resource

from .models import Event

# @admin_required
class Events(Resource):

    def get(self, request, event_id=None, **kwargs):
        json_serializer = serializers.get_serializer('json')()
        if event_id:
            events = json_serializer.serialize(Event.objects.filter(pk=event_id))
        else:
            events = json_serializer.serialize(Event.objects.all())
        return HttpResponse(events, content_type='application/json', status=200)

    def post(self, request, *args, **kwargs):
        Event.objects.create(
            case = 1, 
            volunteer = 1, 
            start = request.POST.get('start'), 
            end = request.POST.get('end'), 
            allDay = request.POST.get('allDay'), 
            title = request.POST.get('title'), 
            description = request.POST.get('description')
            )
        return HttpResponse(status=201)

    def delete(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        event.delete()
        return HttpResponse(status=200)
