from gyms.models import Event
from gyms.config import api_key
from datetime import datetime
import re
import os
import requests
import iso8601
import time


def to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def get_events():
    # insert the api key from teamup.com/api-keys/ 
    resp = requests.get("https://teamup.com/ks13d3ccc86a21d29e/events", timeout=30, headers={
        "Teamup-Token": api_key
    })
    resp.raise_for_status()
    raw_data = resp.json()
    for item in raw_data["events"]:
        # handles some funny business with how the names are formatted
        name = item["title"]
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
        all_day = item["all_day"]
        date = iso8601.parse_date(item["start_dt"])
        notes = item["notes"]
        if not all_day:
            start = to_local(iso8601.parse_date(item["start_dt"]))
            end = to_local(iso8601.parse_date(item["end_dt"]))
            e = Event(name=name, all_day=all_day, date=date, start=start, end=end, notes=notes)
            e.save()
        else:
            e = Event(name = name, all_day = all_day, date = date, in_name_info=in_name_info, notes=notes)
            e.save()