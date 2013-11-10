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
    return ICal_Calendar.genurl(context['request'], protocol=protocol, **kw)
