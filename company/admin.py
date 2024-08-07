from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from .models import Company, Department
from django.utils.html import format_html
from django.contrib import admin
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from employee.models import UserProfile
from .forms import DepartmentForm




# class GetMembersForm(forms.ModelForm):
#     department_members = forms.CharField(
#         label='Department Members',
#         required=False,

#         widget=forms.Textarea(attrs={'readonly': 'readonly', 'rows': 5, 'cols': 50})
#
#     )





    # class Meta:
    #     model = UserProfile
    #     a = UserProfile.objects.filter(department)
    #     fields = ['user_shift', 'role']

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    # extra = 3
    exclude = ('user_shift', 'hire_date', 'role')

class DepartmentAdmin(admin.ModelAdmin):
    change_form_template = 'admin/company/department/department_change_form.html'
    list_display = ('name', 'company', 'department_head', 'get_members')
    form = DepartmentForm

    def change_view(self, request, object_id, form_url='', extra_context=None):
        department = self.get_object(request, object_id)
        if extra_context is None:
            extra_context = {}
        extra_context['department'] = department
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_members(self, obj):
        return ", ".join([profile.user.username for profile in obj.get_members()])

    get_members.short_description = 'Members'




    # def display_members(self, obj):
    #     return ", ".join(obj.get_members())
    #
    # display_members.short_description = 'Members'
    # inlines = [UserProfileInline]


# Register your models here.
admin.site.register(Company)
# admin.site.unregister(Department)
admin.site.register(Department, DepartmentAdmin)



