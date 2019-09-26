import re
import os
import time
from datetime import datetime, timedelta

import iso8601
import pytz
import requests

from gyms.models import Event, EventTime
from gyms.config import api_key


def to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
                                                                now_timestamp)
    return utc_datetime + offset


def format_titles(name):  
    # handles some funny business with how the names are formatted
    in_name_info = ""
    if name.endswith("Hours"):
        name = name.replace(" Hours", "")
    elif name.startswith("CLOSED - "):
        name = name.replace("CLOSED - ", "")
        in_name_info = "closed"
    elif name.endswith(" - CLOSED"):
        name = name.replace(" - CLOSED", "")
        in_name_info = "closed"
    elif name.endswith("-CLOSED"):
        name = name.replace("-CLOSED", "")
        in_name_info = "closed"

    if name.startswith("Pottruck Court"):
        name = "Pottruck Courts"
    elif name.startswith("Pottruck Hours"):
        name = "Pottruck"
    elif name.startswith("Membership"):
        name = "Membership Services"
    return name, in_name_info


def is_open(event):
    if(not event.all_day):
        times = event.eventtime_set.all()
        now = pytz.utc.localize(datetime.now())
        for time in times:
            if now < time.end and now > time.start:
                return True
        return False
    else:
        return event.in_name_info != "closed"


def is_closing(event):
    if(event.open_now):
        now = pytz.utc.localize(datetime.now())
        times = event.eventtime_set.all()
        for time in times:
            if time.end >= now and time.end <= now + timedelta(hours=1):
                return True
        return False


def get_events():
    # insert the api key from teamup.com/api-keys/ 
    resp = requests.get("https://teamup.com/ks13d3ccc86a21d29e/events", 
                        timeout=30, headers={"Teamup-Token": api_key})
    resp.raise_for_status()
    raw_data = resp.json()
    for item in raw_data["events"]:
        name, in_name_info = format_titles(item["title"])
        all_day = item["all_day"]
        date = iso8601.parse_date(item["start_dt"])
        notes = item["notes"]

        e, created = Event.objects.get_or_create(
            name=name
        )
        e.all_day = all_day
        e.date = date
        e.in_name_info = in_name_info
        e.notes = notes
        if not all_day:
            start = to_local(iso8601.parse_date(item["start_dt"]))
            end = to_local(iso8601.parse_date(item["end_dt"]))
            times = EventTime(event=e, start=start, end=end)
            times.save()
        e.save()

    events = list(Event.objects.all())
    for e in events:
        e.open_now = is_open(e)
        e.closing_soon = is_closing(e)
        e.save()
