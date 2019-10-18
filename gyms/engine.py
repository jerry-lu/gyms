import time
from datetime import datetime, timedelta

import iso8601
import pytz
import requests
import re

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
    name = name.replace("Hours", "")

    if re.search(r"\s*-*\s*CLOSED\s*-*\s*", name) is not None:
        name = re.sub(r"\s*-*\s*CLOSED\s*-*\s*", "", name)
        in_name_info = "closed"
    if re.search(r"\s*-*\s*Morning\s*", name) is not None:
        name = re.sub(r"\s*-*\s*Morning\s*", "", name)
    if re.search(r"\s*-*\s*Evening\s*", name) is not None:
        name = re.sub(r"\s*-*\s*Evening\s*", "", name)
    return name.strip(), in_name_info


def is_open(event):
    if(not event.all_day):
        times = event.eventtime_set.all()
        now = pytz.utc.localize(datetime.now())
        for t in times:
            if now < t.end and now > t.start:
                return True
        return False
    else:
        return event.in_name_info != "closed"


def is_closing(event):
    if(event.open_now):
        now = pytz.utc.localize(datetime.now())
        times = event.eventtime_set.all()
        for t in times:
            if t.end >= now and t.end <= now + timedelta(hours=1):
                return True
        return False


def maintain_event_status():
    events = list(Event.objects.all())
    for e in events:
        e.open_now = is_open(e)
        e.closing_soon = is_closing(e)
        e.save()
        if e.date != datetime.today().date():
            e.delete()


def get_events():
    # insert the api key from teamup.com/api-keys/
    resp = requests.get("https://teamup.com/ks13d3ccc86a21d29e/events",
                        timeout=30, headers={"Teamup-Token": api_key})
    resp.raise_for_status()
    raw_data = resp.json()
    for item in raw_data["events"]:
        name, in_name_info = format_titles(item["title"])
        all_day = item["all_day"]
        notes = item["notes"]

        e, created = Event.objects.get_or_create(name=name,
                                                 date=datetime.today(),
                                                 all_day=all_day,
                                                 in_name_info=in_name_info,
                                                 notes=notes)
        e.save()
        if not all_day:
            start = to_local(iso8601.parse_date(item["start_dt"]))
            end = to_local(iso8601.parse_date(item["end_dt"]))
            times, created = EventTime.objects.get_or_create(event=e,
                                                             start=start,
                                                             end=end)
            times.save()

    maintain_event_status()
