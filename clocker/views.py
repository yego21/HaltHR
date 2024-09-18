# views.py
import logging
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from .models import Clocker
from employee.models import UserProfile
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponse
from django.core.management import call_command
from exporter.exports import export_clocker_to_csv, export_clocker_to_xls


@login_required
def clock_in(request):
    if request.method == "POST":
        user = request.user
        today = timezone.localdate()
        has_clocked_in = Clocker.objects.filter(user=user, date=today, time_in__isnull=False).first()
        has_clocked_out = Clocker.objects.filter(user=user, date=today, time_out__isnull=False).first()

        if has_clocked_in:
            return HttpResponse(
                f'<p style="color: red;">{user.username} has already clocked in for today, please proceed to clock out or contact your system administrator.</p>',
                content_type='text/html')
            # return JsonResponse({'status': 'failure', 'message': f'{user.username} has already clocked in for today, please proceed to clock out or contact your system administrator'})
            # print(f"existing clocker = true, existing shift = true,")

        else:
            # User does not have a time_in recorded, record new clock in
            time_in = timezone.now()
            clocker = Clocker(user=user, date=today, time_in=time_in)
            clocker.save()
            return HttpResponse('Clock in time recorded successfully.')
            print("Clock in time recorded successfully.")
            # messages.success(request, f'{user.username} clocked in at {time_in}.')

        return redirect(reverse('index'))


@login_required
def clock_out(request):
    user = request.user
    today = timezone.localdate()
    has_clocked_in = Clocker.objects.filter(user=user, date=today, time_in__isnull=False, time_out__isnull=True).first()
    has_clocked_out = Clocker.objects.filter(user=user, date=today, time_out__isnull=False).first()
    context = {
        'has_clocked_in': has_clocked_in is not None,
        'response': HttpResponse('Clock out time recorded successfully.')
    }

    if has_clocked_out:
        return HttpResponse(f'{user.username} has already clocked out for today, record not submitted.')
    else:
        if has_clocked_in:
            # User has a time_in recorded but no time_out yet
            has_clocked_in.time_out = timezone.now()
            has_clocked_in.save()
            return HttpResponse('Clock out time recorded successfully.')

        else:
            confirm = request.POST.get('confirm')
            confirmed_clock_out = False
            if confirm == 'yes':
                time_out = timezone.now()
                clocker = Clocker(user=user, time_out=time_out)
                clocker.save()
                print('confirm-yes')
                confirmed_clock_out = True
                return HttpResponse('Clock out confirmed')

            if not confirmed_clock_out:
                response = JsonResponse({'status': 'confirm',
                                         'message': f'{user.username} does not have Clock in record for today, are you sure you want to Clock out?'})
                return response

            # elif confirmed_clock_out:
            #     response = HttpResponse('Clock out confirmed')
            #     return response

        # return HttpResponse("You don't have Clock in record for today, are you sure to Clock out?")
        # messages.warning(request,f' does not have Clock in record for today, are you sure to Clock out?')
        # return redirect('index')

    # return redirect(reverse('index'))


def clocker_entries(request):
    user_id = request.GET.get('user_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter queryset based on parameters
    queryset = Clocker.objects.all()
    # if start_date and end_date:
    #     queryset = queryset.filter(date__range=[start_date, end_date])
    # if user_id:
    #     queryset = queryset.filter(user_id=user_id)

    return render(request, 'clocker/clocker_entries.html', {'user_id': user_id})

    # Query the clocker entries
    user_clockers = Clocker.objects.filter(user_id=user_id, date__range=[start_date, end_date])
    # results = [clocker.to_dict() for clocker in clockers]  # Ensure to_dict() or similar method exists    #
    # return JsonResponse(results, safe=False)
    # return redirect(reverse('admin/clocker/clocker', args=[user_id]))


def clocker_popup(request, user_id):
    # clocker = get_object_or_404(Clocker, pk=pk)

    user_clocker = Clocker.objects.filter(user_id=user_id)
    user = UserProfile.objects.get(user_id=user_id)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        user_clocker = Clocker.objects.filter(user_id=user_id)
        user_clocker = user_clocker.filter(date__range=[start_date, end_date])
    else:
        user_clocker = None
    user = get_object_or_404(UserProfile, user_id=user_id)

    if 'export_clocker_csv' in request.GET:
        return export_clocker_to_csv(user_clocker, user)

    if 'export_clocker_xls' in request.GET:
        return export_clocker_to_xls(user_clocker, user)

    return render(request, 'clocker/clocker_popup.html', {'user_clocker': user_clocker, 'user': user})


def attendance_logs(request, user_id):
    # clocker = get_object_or_404(Clocker, pk=pk)

    user_clocker = Clocker.objects.filter(user_id=user_id)
    user = UserProfile.objects.get(user_id=user_id)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        user_clocker = Clocker.objects.filter(user_id=user_id)
        user_clocker = user_clocker.filter(date__range=[start_date, end_date])
    else:
        user_clocker = None
    user = get_object_or_404(UserProfile, user_id=user_id)

    if 'export_clocker_csv' in request.GET:
        return export_clocker_to_csv(user_clocker, user)

    if 'export_clocker_xls' in request.GET:
        return export_clocker_to_xls(user_clocker, user)

    return render(request, 'clocker/view_attendance_logs.html', {'user_clocker': user_clocker, 'user': user})


def htmx_view(request):
    return render(request, 'tester.html')
