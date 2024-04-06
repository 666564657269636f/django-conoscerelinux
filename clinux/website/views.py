from django.db.models import Max
from django.shortcuts import render
from django.utils import timezone
from events.models import Event
from pages.models import StaticPage


def index(request):
    # Search for events that have at least a session which start in the future
    events = Event.objects.annotate(start=Max("sessions__start")).filter(
        start__gte=timezone.now()
    )
    context = {"message": "World!", "events": events}
    return render(request, "index.html", context)
