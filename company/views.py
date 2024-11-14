# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Event, Event_Media, Event_Schedule, Career
from django.views.generic import ListView



@login_required
def view_members(request):
    return render(request, 'company/department/department_change_form.html')


def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    media = Event_Media.objects.filter(event=event)
    event_schedule = Event_Schedule.objects.filter(event=event)
    # Get the previous event
    previous_event = Event.objects.filter(event_schedule__lt=event_schedule.first()).order_by('-event_schedule').first()

    # Get the next event
    next_event = Event.objects.filter(event_schedule__gt=event_schedule.first()).order_by('event_schedule').first()

    context = {
        'event': event,
        'previous_event': previous_event,
        'next_event': next_event,
        'media': media,
        'event_schedule': event_schedule
    }
    return render(request, 'company/event/event_details_partial.html', context)


def load_media(request, media_id):
    event_media = get_object_or_404(Event_Media, id=media_id)

    previous_media = Event_Media.objects.filter(event_id=event_media.event_id, id__lt=event_media.id).order_by(
        '-id').first()
    next_media = Event_Media.objects.filter(event_id=event_media.event_id, id__gt=event_media.id).order_by('id').first()

    context = {
        'event_media': event_media,
        'previous_media': previous_media,
        'next_media': next_media,
    }

    return render(request, 'company/event/event_media_viewer.html', context)

class CareerListView(ListView):
    model = Career
    template_name = 'company/career/careers.html'  # Define the template path
    context_object_name = 'careers'  # Optional: To rename the default 'object_list'
    paginate_by = 10  # Optional: Add pagination (10 jobs per page)
