from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('clock-in/', views.clock_in, name='clock-in'),
    path('clock-out/', views.clock_out, name='clock-out'),
    # path('clocker/', ClockerListView.as_view(), name='clocker_list'),
    path('admin/clocker/filter-clocker/<int:user_id>', views.clocker_entries, name='clocker_entries'),
    path('clocker_popup/<int:user_id>/', views.clocker_popup, name='clocker_popup'),
    path('index', views.htmx_view, name='htmx_view')
]