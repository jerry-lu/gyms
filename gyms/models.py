from django.db import models
from django.utils import timezone
from datetime import datetime


class Event(models.Model):
    name = models.CharField(max_length=200)
    all_day = models.BooleanField(default=True)
    in_name_info = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    notes = models.CharField(max_length=500, null=True)
    open_now = models.BooleanField(default=False)
    closing_soon = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class EventTime(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              related_name="times")
    start = models.DateTimeField()
    end = models.DateTimeField()
