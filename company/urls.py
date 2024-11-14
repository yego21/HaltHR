from django.urls import path
from . import views



urlpatterns = [
    # path('admin/company/department/<int:pk>/', views.view_members, name='view_members'),
    path('event_details/<int:event_id>/', views.event_details, name='event_details'),
    path('media/load/<int:media_id>/', views.load_media, name='load_media'),
    path('careers/', views.CareerListView.as_view(), name='careers'),
]
