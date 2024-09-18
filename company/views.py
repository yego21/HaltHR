# views.py
import logging
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from .models import Department
from employee.models import UserProfile
from django.utils import timezone
from django.http import JsonResponse
from .models import Event, Event_Media



#
# def view_department_members(request, department_id):
#     # Retrieve the department based on the department_id from the URL
#     department = get_object_or_404(Department, id=department_id)
#
#     # Get all UserProfiles associated with this department
#     members = UserProfile.objects.filter(department=department)
#
#     # Pass the department and members to the template
#     context = {
#         'department': department,
#         'members': members
#     }
#
#     return render(request, 'department_members.html', context)

@login_required
def view_members(request):
    return render(request, 'company/department/department_change_form.html')


def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    media = Event_Media.objects.filter(event=event)


    # Get the previous event
    previous_event = Event.objects.filter(date__lt=event.date).order_by('-date').first()

    # Get the next event
    next_event = Event.objects.filter(date__gt=event.date).order_by('date').first()

    context = {
        'event': event,
        'previous_event': previous_event,
        'next_event': next_event,
        'media': media
    }
    return render(request, 'company/event/event_details_partial.html', context)

def load_media(request, media_id):
    event_media = get_object_or_404(Event_Media, id=media_id)

    previous_media = Event_Media.objects.filter(event_id=event_media.event_id, id__lt=event_media.id).order_by('-id').first()
    next_media = Event_Media.objects.filter(event_id=event_media.event_id, id__gt=event_media.id).order_by('id').first()

    context = {
        'event_media': event_media,
        'previous_media': previous_media,
        'next_media': next_media,
    }


    return render(request, 'company/event/event_media_viewer.html', context)









