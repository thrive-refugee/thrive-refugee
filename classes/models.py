from django.db import models


class WalkinClass(models.Model):
    name = models.CharField("Name", max_length=50)

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __unicode__(self):
        return self.name


class Attendee(models.Model):
    name = models.CharField("Name", max_length=50)
    phone = models.CharField("Phone Number", max_length=80)

    class Meta:
        verbose_name = 'Attendee'
        verbose_name_plural = 'Attendees'

    def __unicode__(self):
        return self.name


class Session(models.Model):
    start_date_time = models.DateTimeField()
    stop_date_time = models.DateTimeField()
    teacher = models.ForeignKey('refugee_manager.Volunteer', on_delete=models.SET_NULL, blank=True, null=True,)
    members = models.ManyToManyField(
        Attendee,
        through='Attendance',
        through_fields=('session', 'attendee'),
    )
    walk_in_class = models.ForeignKey(WalkinClass, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.walk_in_class.name + " " + unicode(self.start_date_time)


class Attendance(models.Model):
    notes = models.TextField("Notes", blank=True)

    start_date_time = models.DateTimeField()
    stop_date_time = models.DateTimeField(blank=True, null=True)

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('attendee', 'session'),)
