from django.shortcuts import render
from django.http import HttpResponse
from gyms.models import Event
from gyms.engine import get_events


def index(request):
    Event.objects.all().delete()
    get_events()
    events = list(Event.objects.all().order_by('name'))
    events = sorted(events, key=lambda x: x.open_now(), reverse=True)
    return render(request, "index.html", {"events": events})
