from django.db import models
from django.utils import timezone


class Event(models.Model):
    name = models.CharField(max_length=200)
    all_day = models.BooleanField(default=True)
    in_name_info = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    notes = models.CharField(max_length=500, null=True, blank=True)
    open_now = models.BooleanField(default=False, null=True, blank=True)
    closing_soon = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class EventTime(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.start.strftime('%Y-%m-%d %H:%M')
