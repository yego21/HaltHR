import logging
from django import forms
from employee.models import UserProfile
from .models import Department
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse

# Set up logging
logger = logging.getLogger(__name__)

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Get the department instance
        department = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        logger.debug(f'Available fields: {self.fields.keys()}')
        logger.debug(f'Department instance: {department}')
        # if has_perm('company.change_department'):
        if department and hasattr(department, 'department_head'):
            try:
                # Filter UserProfiles to include only members of the current department
                self.fields['department_head'].queryset = UserProfile.objects.filter(department=department)
            except Exception as e:
                logger.error(f'Error filtering department head queryset: {e}')
                self.fields['department_head'].queryset = UserProfile.objects.none()
        else:
            # Default queryset when no department instance is available or accessible
            self.fields['department_head'].queryset = UserProfile.objects.none()

