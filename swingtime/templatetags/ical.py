"""
Defines template tag ical, as in:

{% ical %}

{% ical "http" %}
"""
from django import template
from ..models import ICal_Calendar

register = template.Library()

@register.simple_tag(takes_context=True)
def ical(context, protocol='webcal', **kw):
	if 'user' in context:
		user = context['user']
	elif 'request' in context:
		user = context['request'].user
	else:
		raise IndexError("Misconfigured context processors, can't find current user")
	return ICal_Calendar.genurl(user, protocol=protocol, **kw)
