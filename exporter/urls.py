from django.urls import path
from .views import export_clocker_entries

urlpatterns = [
    path('export/', export_clocker_entries, name='export_clocker_entries'),
]
