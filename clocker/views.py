# views.py

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Clocker
from datetime import datetime
from django.http import JsonResponse
from django.core.management import call_command

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def clock_in(request):
    user = request.user

    # Example of handling clock in logic
    now = datetime.now()
    call_command('ClockIn')
    return JsonResponse({'message': 'Clockin command executed'}, status=200)
    # return redirect('index')

@login_required
def clock_out(request):
    user = request.user

    # Example of handling clock out logic
    user = request.user

    # Example of handling clock in logic
    now = datetime.now()
    call_command('ClockOut')
    return redirect({'message': 'ClockOut command executed', 'redirect_url': reverse('index')})

    # return redirect('index')
