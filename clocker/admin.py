from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin
from django.contrib.auth.models import User
from .models import Clocker
from django.utils.dateparse import parse_date

class ClockerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'time_in', 'time_out', 'get_remarks')

    def get_remarks(self, obj):
        return obj.calculate_time_difference
    get_remarks.short_description = 'Remarks'

    def get_full_name(self, instance):
        return instance.user.userprofile.full_name

    get_full_name.short_description = 'Full Name'

    # calculate_time_difference.short_description = "View Clocker Records"
    # readonly_fields = ('get_shift_name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        user_id = request.GET.get('user')

        if start_date and end_date and user_id:
            try:
                start_date = parse_date(start_date)
                end_date = parse_date(end_date)
            except ValueError:
                return qs  # Return unfiltered queryset if date parsing fails

            qs = qs.filter(user_id=user_id, timestamp__range=(start_date, end_date))

        return qs


admin.site.register(Clocker, ClockerAdmin)






