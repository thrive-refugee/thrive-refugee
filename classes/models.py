from django.db import models


class WalkinClass(models.Model):
    Name = models.CharField("Name", max_length=50)
    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'


class Attendee(models.Model):
    Name = models.CharField("Name", max_length=50)
    Phone = models.CharField("Phone Number", max_length=80)

    class Meta:
        verbose_name = 'Attendee'
        verbose_name_plural = 'Attendees'

    def __unicode__(self):
        return self.Name


class Session(models.Model):
    Start_Date_Time = models.DateTimeField()
    StopDateTime = models.DateTimeField()
    Teacher = models.ForeignKey('refugee_manager.Volunteer', on_delete=models.SET_NULL, blank=True, null=True,)
    members = models.ManyToManyField(
        Attendee,
        through='Attendance',
        through_fields=('session', 'attendee'),
    )


class Attendance(models.Model):
    Notes = models.TextField("Notes")

    StartDateTime = models.DateTimeField(auto_now_add=True)
    StopDateTime = models.DateTimeField(blank=True, null=True)

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('attendee', 'session'),)
