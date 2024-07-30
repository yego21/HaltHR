# views.py
import logging
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from .models import Clocker
from employee.models import UserProfile
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.management import call_command






@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def clock_in(request):
    user = request.user
    today = timezone.localdate()
    has_clocked_in = Clocker.objects.filter(user=user, date=today, time_in__isnull=False).first()
    has_clocked_out = Clocker.objects.filter(user=user, date=today, time_out__isnull=False).first()

    if has_clocked_in:
        return JsonResponse({'status': 'failure', 'message': f'{user.username} has already clocked in for today, please proceed to clock out or contact your system administrator'})
        print(f"existing clocker = true, existing shift = true,")

    else:
        # User does not have a time_in recorded, record new clock in
        time_in = timezone.now()
        clocker = Clocker(user=user, date=today, time_in=time_in)
        clocker.save()
        return JsonResponse({'status': 'success', 'message': 'Clock in time recorded successfully.'})
        print("Clock in time recorded successfully.")
        # messages.success(request, f'{user.username} clocked in at {time_in}.')

    return redirect(reverse('index'))

@login_required
def clock_out(request):
    user = request.user
    today = timezone.localdate()
    has_clocked_in = Clocker.objects.filter(user=user, date=today, time_in__isnull=False, time_out__isnull=True).first()
    has_clocked_out = Clocker.objects.filter(user=user, date=today, time_out__isnull=False).first()

    if has_clocked_out:
        return JsonResponse({'status': 'failure',
                             'message': f'{user.username} has already clocked out for today, record not submitted.'})
    else:
        if has_clocked_in:
            # User has a time_in recorded but no time_out yet
            has_clocked_in.time_out = timezone.now()
            has_clocked_in.save()
            return JsonResponse({'status': 'success', 'message': 'Clock out time recorded successfully.'})

        else:
            confirm = request.POST.get('confirm')
            if confirm == 'yes':
                time_out = timezone.now()
                clocker = Clocker(user=user, time_out=time_out)
                clocker.save()
                # messages.warning(request,
                #                  f'{user.username} does not have Clock in record for today, are you sure to Clock out?')
                return JsonResponse({'status': 'success', 'message': 'Clock out time recorded successfully.'})

            else:
                # return redirect('index')
                return JsonResponse({'status': 'confirm',
                                     'message': f'{user.username} does not have Clock in record for today, are you sure you want to Clock out?'})


            # messages.warning(request,f'{user.username} does not have Clock in record for today, are you sure to Clock out?')
            return redirect('index')
    return redirect(reverse('index'))


