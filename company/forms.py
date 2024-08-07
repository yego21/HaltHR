# company/forms.py

from django import forms
from employee.models import UserProfile
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Get the department instance
        department = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if department:
            # Filter UserProfiles to include only members of the current department
            self.fields['department_head'].queryset = UserProfile.objects.filter(department=department)
        else:
            # Default queryset when no department instance is available
            self.fields['department_head'].queryset = UserProfile.objects.none()
