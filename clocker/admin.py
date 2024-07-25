from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin
from django.contrib.auth.models import User
from .models import Clocker

admin.site.register(Clocker)


# Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.unregister(UserAdmin)
# admin.site.register(User, UserAdmin)