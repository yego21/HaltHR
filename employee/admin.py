from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Shift
from clocker.models import Clocker
admin.site.register(Shift)
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from datetime import datetime
# admin.site.unregister(UserProfile)



class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Role'
    readonly_fields = ('is_department_head_display',)

    def is_department_head_display(self, instance):
        return instance.is_department_head

    is_department_head_display.short_description = 'Department Head'






#Define a new User admin
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_user_shift',)
    list_select_related = ('userprofile',)

    def get_user_shift(self, instance):
        return instance.userprofile.user_shift
    get_user_shift.short_description = 'Shift'





class UserProfileAdmin(admin.ModelAdmin):
    change_form_template = 'admin/employee/userprofile/userprofile_change_form.html'
    list_display = ('full_name', 'department', 'position', 'user_shift')
    # readonly_fields = ('position_display', 'full_name_display', 'hire_date')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Get the UserProfile object based on the object_id
        user_profile = get_object_or_404(UserProfile, id=object_id)

        # Add the user_profile object to the extra_context
        if extra_context is None:
            extra_context = {}
        extra_context['user_profile'] = user_profile

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def full_name_display(self, obj):
        full_name = obj.user
        return f'{full_name.first_name} {full_name.last_name}'
    full_name_display.short_description = 'Full Name'


    # def position_display(self, instance):
    #     if instance.is_department_head is None:
    #         return 'None'
    #     return 'Department Head' if instance.is_department_head else 'Member'

    # position_display.short_description = 'Position'










admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)


# Register your models here.
