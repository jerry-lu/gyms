from django.db import models
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
import pytz

class Event(models.Model):
    name = models.CharField(max_length=200)
    all_day = models.BooleanField()
    in_name_info = models.CharField(max_length=200, blank = True, null = True)
    date = models.DateField(default = timezone.now)
    start = models.DateTimeField(blank = True, null = True)
    end = models.DateTimeField(blank = True, null = True)

    def __str__(self):
       return self.name
    def open_now(self):
        if(not self.all_day):
            now = pytz.utc.localize(datetime.now())
            return now < self.end and now > self.start
        else:
            return self.in_name_info != "closed"
    def closing_soon(self):
        if(self.open_now()):
            now = pytz.utc.localize(datetime.now())
            return self.end <= now + timedelta(hours=1)