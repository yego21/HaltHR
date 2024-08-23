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
from .models import Event


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










