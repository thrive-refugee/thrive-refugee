import string
import random
import logging

from datetime import datetime
from functools import total_ordering

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db.models import Q

from dateutil import rrule

import refugee_manager.models as refugee_models
import employment_manager.models as employment_models


__all__ = (
    'EventType',
    'Event',
    'Occurrence',
    'ICal_Calendar',
    'create_event'
)


class EventType(models.Model):

    """Simple ``Event`` classifcation."""
    abbr = models.CharField(_('abbreviation'), max_length=4, unique=True)
    label = models.CharField(_('label'), max_length=50)

    class Meta:
        verbose_name = _('event type')
        verbose_name_plural = _('event types')

    def __unicode__(self):
        return self.label


class EventQuerySet(models.query.QuerySet):

    def for_user(self, user):
        if user.is_superuser:
            rv = self.all()
        else:
            try:
                rv = self.filter(
                    Q(refugee_case__volunteers=user.volunteer) |
                    Q(employment_case__volunteers=user.volunteer) |
                    Q(refugee_case=None, employment_case=None)
                )
            except refugee_models.Volunteer.DoesNotExist:
                rv = self.filter(refugee_case=None, employment_case=None)
        return rv


class EventManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return EventQuerySet(self.model)

    def for_user(self, user):
        return self.get_queryset().for_user(user)


class AutoCase(object):

    def __get__(self, obj, type=None):  # pylint: disable=W0622
        rv = None
        try:
            rv = obj.refugee_case
        except AttributeError as exc:
            logging.exception(exc)
        if rv is None:
            rv = obj.employment_case
        return rv

    def __set__(self, obj, value):
        if value is None:
            obj.refugee_case = None
            obj.employment_case = None
        elif isinstance(value, refugee_models.Case):
            obj.refugee_case = value
            obj.employment_case = None
        elif isinstance(value, refugee_models.Case):
            obj.refugee_case = None
            obj.employment_case = value
        else:
            raise TypeError("Case cannot be a {} object".format(type(value).__name__))


class Event(models.Model):
    '''
    Container model for general metadata and associated ``Occurrence`` entries.
    '''
    title = models.CharField(_('title'), max_length=32)
    description = models.CharField(_('description'), max_length=100)
    event_type = models.ForeignKey(EventType, verbose_name=_('event type'), null=True, blank=True)
    refugee_case = models.ForeignKey(refugee_models.Case, null=True, blank=True, db_index=True)
    employment_case = models.ForeignKey(employment_models.EmploymentClient, null=True, blank=True, db_index=True)

    case = AutoCase()

    objects = EventManager()

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ('title',)

    def clean(self):
        if self.refugee_case and self.employment_case:
            raise ValidationError(
                "Cannot have both a Refugee and Employment case")

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('swingtime-event', [str(self.id)])

    def add_occurrences(self, start_time, end_time, address, **rrule_params):
        """Add one or more occurences to the event using a comparable API to
        ``dateutil.rrule``.

        If ``rrule_params`` does not contain a ``freq``, one will be defaulted
        to ``rrule.DAILY``.

        Because ``rrule.rrule`` returns an iterator that can essentially be
        unbounded, we need to slightly alter the expected behavior here in order
        to enforce a finite number of occurrence creation.

        If both ``count`` and ``until`` entries are missing from ``rrule_params``,
        only a single ``Occurrence`` instance will be created using the exact
        ``start_time`` and ``end_time`` values.

        """
        rrule_params.setdefault('freq', rrule.DAILY)

        if 'count' not in rrule_params and 'until' not in rrule_params:
            self.occurrence_set.create(start_time=start_time, end_time=end_time, address=address)
        else:
            delta = end_time - start_time
            for ev in rrule.rrule(dtstart=start_time, **rrule_params):
                self.occurrence_set.create(start_time=ev, end_time=ev + delta, address=address)

    def upcoming_occurrences(self):
        '''
        Return all occurrences that are set to start on or after the current
        time.
        '''
        return self.occurrence_set.filter(start_time__gte=datetime.now())

    def next_occurrence(self):
        '''
        Return the single occurrence set to start on or after the current time
        if available, otherwise ``None``.
        '''
        upcoming = self.upcoming_occurrences()
        return upcoming and upcoming[0] or None

    def daily_occurrences(self, dt=None):
        '''
        Convenience method wrapping ``Occurrence.objects.daily_occurrences``.
        '''
        return Occurrence.objects.daily_occurrences(dt=dt, event=self)


class OccurrenceQuerySet(models.query.QuerySet):

    def daily_occurrences(self, dt=None, event=None):
        '''
        Returns a queryset of for instances that have any overlap with a
        particular day.

        * ``dt`` may be either a datetime.datetime, datetime.date object, or
          ``None``. If ``None``, default to the current day.

        * ``event`` can be an ``Event`` instance for further filtering.
        '''
        dt = dt or datetime.now()
        start = datetime(dt.year, dt.month, dt.day)
        end = start.replace(hour=23, minute=59, second=59)
        qs = self.filter(
            models.Q(
                start_time__gte=start,
                start_time__lte=end,
            ) |
            models.Q(
                end_time__gte=start,
                end_time__lte=end,
            ) |
            models.Q(
                start_time__lt=start,
                end_time__gt=end
            )
        )

        return qs.filter(event=event) if event else qs

    def for_user(self, user):
        if user.is_superuser:
            rv = self
        else:
            try:
                rv = self.filter(
                    Q(event__refugee_case__volunteers=user.volunteer) |
                    Q(event__employment_case__volunteers=user.volunteer) |
                    Q(event__refugee_case=None, event__employment_case=None)
                )
            except refugee_models.Volunteer.DoesNotExist:
                rv = self.filter(
                    event__refugee_case=None, employment_case=None)
        return rv


class OccurrenceManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return OccurrenceQuerySet(self.model)

    def daily_occurrences(self, dt=None, event=None):
        return self.get_queryset().daily_occurrences(dt, event)

    def for_user(self, user):
        return self.get_queryset().for_user(user)


@total_ordering
class Occurrence(models.Model):

    """Represents the start end time for a specific occurrence of a master
    ``Event`` object."""
    start_time = models.DateTimeField(_('start time'))
    end_time = models.DateTimeField(_('end time'))
    event = models.ForeignKey(Event, verbose_name=_('event'), editable=False)
    address = models.CharField(max_length=255, blank=True, null=True)

    objects = OccurrenceManager()

    class Meta:
        verbose_name = _('occurrence')
        verbose_name_plural = _('occurrences')
        ordering = ('start_time', 'end_time')

    def __unicode__(self):
        return '%s: %s' % (self.title, self.start_time.isoformat())

    @models.permalink
    def get_absolute_url(self):
        return ('swingtime-occurrence', [str(self.event.id), str(self.id)])

    def __eq__(self, other):
        return self.start_time == other.start_time

    def __lt__(self, other):
        return self.start_time < other.start_time

    @property
    def title(self):
        return self.event.title

    @property
    def event_type(self):
        return self.event.event_type


def create_event(
    title,
    event_type,
    description='',
    start_time=None,
    end_time=None,
    address='',
    case=None,
    **rrule_params
):
    '''
    Convenience function to create an ``Event``, optionally create an
    ``EventType``, and associated ``Occurrence``s. ``Occurrence`` creation
    rules match those for ``Event.add_occurrences``.

    Returns the newly created ``Event`` instance.

    Parameters

    ``event_type``
        can be either an ``EventType`` object or 2-tuple of ``(abbreviation,label)``,
        from which an ``EventType`` is either created or retrieved.

    ``start_time``
        will default to the current hour if ``None``

    ``end_time``
        will default to ``start_time`` plus swingtime_settings.DEFAULT_OCCURRENCE_DURATION
        hour if ``None``

    ``freq``, ``count``, ``rrule_params``
        follow the ``dateutils`` API (see http://labix.org/python-dateutil)

    '''
    from swingtime.conf import settings as swingtime_settings

    if isinstance(event_type, tuple):
        event_type, _created = EventType.objects.get_or_create(
            abbr=event_type[0],
            label=event_type[1]
        )

    event = Event.objects.create(
        title=title,
        description=description,
        event_type=event_type
    )
    event.case = case

    start_time = start_time or datetime.now().replace(
        minute=0,
        second=0,
        microsecond=0
    )

    end_time = end_time or start_time + swingtime_settings.DEFAULT_OCCURRENCE_DURATION
    event.add_occurrences(start_time, end_time, **rrule_params)
    return event


def genslug():
    return ''.join(ICal_Calendar._random.choice(string.uppercase) for _ in range(32))


class ICal_Calendar(models.Model):
    slug = models.CharField(max_length=32, primary_key=True, default=genslug)
    volunteer = models.ForeignKey(refugee_models.Volunteer)
    everything = models.BooleanField(default=False)

    _random = random.SystemRandom()

    @classmethod
    def genurl(cls, request, everything=False, protocol=None):
        """ICal_Calendar.genurl(Request) -> str
        Find/create a calendar for the given user and return the URL to it.
        """
        user = request.user
        if not user.is_superuser:
            everything = False
        v = user.volunteer
        cal, _ = ICal_Calendar.objects.get_or_create(volunteer=v, everything=everything)

        url = request.build_absolute_uri(reverse('swingtime.views.ics_feed', kwargs={'slug': cal.slug}))

        if protocol is not None:
            if url.startswith('http:'):
                url = protocol + ':' + url[len('http:'):]
        return url

    @classmethod
    def genwebcal(cls, request, everything=False):
        return cls.genurl(request, everything, protocol='webcal')

# Doesn't actually seem to be called?


@receiver(post_save, sender=User)
def remove_ical(sender, instance, created, raw, using, **kw):
    print(sender, instance, created, raw, using, kw)
    if not instance.is_active:
        ICal_Calendar.objects.filter(volunteer=instance.volunteer).delete()
