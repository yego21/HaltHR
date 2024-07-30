from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin
from django.contrib.auth.models import User
from .models import Clocker

class ClockerAdmin(admin.ModelAdmin):
    list_display = ('user', 'time_in', 'time_out', 'calculate_time_difference')
    # readonly_fields = ('get_shift_name',)


admin.site.register(Clocker, ClockerAdmin)






