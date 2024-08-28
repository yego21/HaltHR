from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('userprofile/', views.UserProfileView.as_view(), name='userprofile'),
    path('userprofile/edit/', views.UserProfileUpdateView.as_view(), name='userprofile_edit'),
]