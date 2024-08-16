from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from .models import Company, Department
from django.utils.html import format_html
from django.contrib import admin
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from employee.models import UserProfile
from .forms import DepartmentForm
from django.http import HttpResponseForbidden
from django import forms



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

    # def get_members(self, obj):
    #     return ", ".join([profile.user.username for profile in obj.get_members()])

    # get_members.short_description = 'Members'




    # def display_members(self, obj):
    #     return ", ".join(obj.get_members())
    #
    # display_members.short_description = 'Members'
    # inlines = [UserProfileInline]


# Register your models here.
admin.site.register(Company)
# admin.site.unregister(Department)
admin.site.register(Department, DepartmentAdmin)



