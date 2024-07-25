from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('clock-in/', views.clock_in, name='clock-in'),
    path('clock-out/', views.clock_out, name='clock-out'),
]