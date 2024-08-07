from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Shift

admin.site.register(Shift)
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
    list_display = ('full_name', 'department', 'position_display')
    readonly_fields = ('position_display', 'full_name_display')

    def full_name_display(self, obj):
        full_name = obj.user
        return f'{full_name.first_name} {full_name.last_name}'

    def position_display(self, instance):
        return instance.is_department_head




    position_display.short_description = 'Position'









admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)


# Register your models here.
