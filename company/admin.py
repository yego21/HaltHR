from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from .models import Company, Department, Event, Announcement, Event_Media, Event_Schedule, Career
from django.utils.html import format_html
from django.contrib import admin
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from employee.models import UserProfile
from .forms import DepartmentForm
from django.http import HttpResponseForbidden
from django import forms
import json



class Event_MediaInline(admin.StackedInline):
    model = Event_Media
    extra = 1

class Event_ScheduleInline(admin.StackedInline):
    model = Event_Schedule
    extra = 1


# class EventAdminForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = '__all__'
#
#
#     def clean_event_dates(self):
#         dates = self.data.getlist('date[]')
#         times = self.data.getlist('time[]')
#         descriptions = self.data.getlist('event_dates[]')
#         cleaned_dates = []
#
#         existing_dates = self.cleaned_data.get('event_dates', [])
#         print(existing_dates)
#
#
#         for date, time, description in zip(dates, times, descriptions):
#             if date and time and description:  # Check if all fields have been filled
#                 cleaned_dates.append({
#                     'date': date,
#                     'time': time,
#                     'description': description,
#                 })
#
#                 cleaned_dates.extend(existing_dates)
#             elif not existing_dates:
#                     raise forms.ValidationError('All fields for each date entry must be filled.')
#             else:
#                 cleaned_dates = existing_dates
#
#
#
#
#
#
#
#         # Get new date, time, and description from the POST request data (form inputs)
#         # If there is new data, append it as a new entry to the event dates
#         existing_dates = []
#
#         # Save the combined dates back to the event
#
#         return cleaned_dates





class EventAdmin(admin.ModelAdmin):
    # change_form_template = 'admin/company/event/event_change_form.html'
    model = Event
    # form = EventAdminForm
    inlines = [Event_ScheduleInline, Event_MediaInline]




class UserProfileInline(admin.StackedInline):
    model = UserProfile
    # extra = 3
    exclude = ('user_shift', 'hire_date', 'role')

class DepartmentAdmin(admin.ModelAdmin):
    form = DepartmentForm
    change_form_template = 'admin/company/department/department_change_form.html'
    list_display = ('name', 'company', 'department_head')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Filter departments based on user's profile
        if request.user.is_superuser:
            return qs  # Superusers see all departments
        else:
            # Assuming UserProfile has a ForeignKey to Department
            # and the user has one UserProfile
            # from employee.models import UserProfile
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                return qs.filter(id=user_profile.department.id)
            except UserProfile.DoesNotExist:
                return qs.none()  # Return an empty queryset if no profile is found

    def get_form(self, request, obj=None, **kwargs):
        """
        Return the form class to use in the admin change form based on permissions.
        """
        if obj and not request.user.has_perm('company.change_department'):
            # User does not have change permission; use a form without the filter
            class ReadOnlyDepartmentForm(forms.ModelForm):
                class Meta:
                    model = Department
                    fields = '__all__'

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    # Set queryset for department_head to all UserProfiles
                    self.fields['department_head'].queryset = UserProfile.objects.all()

            return ReadOnlyDepartmentForm

        # User has change permission; use the regular form
        return super().get_form(request, obj, **kwargs)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Handle the change view, including permission checks.
        """
        department = self.get_object(request, object_id)
        if extra_context is None:
            extra_context = {}
        extra_context['department'] = department
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def response_change(self, request, obj):
        # Custom redirection logic
        # Redirecting to the change list view if the user lacks permission
        return HttpResponseRedirect(reverse('admin:company_department_changelist'))




# Register your models here.
# admin.site.register(Company)
# admin.site.unregister(Event)
admin.site.register(Event, EventAdmin)
admin.site.register(Announcement)
# admin.site.unregister(Department)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Event_Media)
admin.site.register(Event_Schedule)
admin.site.register(Career)


admin.site.register(Company)