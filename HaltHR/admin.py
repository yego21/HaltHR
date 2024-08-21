from django.contrib import admin
from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = "Your Custom Admin"
    site_title = "Your Admin"
    index_title = "Welcome to Your Admin"

    class Media:
        css = {
            'all': ('css/custom_admin.css',),
        }

admin_site = CustomAdminSite(name='custom_admin')