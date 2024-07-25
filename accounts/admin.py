from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Shift

admin.site.register(Shift)
admin.site.register(UserProfile)
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_shift')
    list_select_related = ('userprofile',)

    def get_shift(self, instance):
        return instance.userprofile.shift

    get_shift.short_description = 'Shift'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
