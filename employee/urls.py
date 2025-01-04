from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('userprofile/', views.UserProfileView.as_view(), name='userprofile'),
    # path('userprofile/edit/', views.UserProfileUpdateView.as_view(), name='userprofile_edit'),
    path('userprofile/<int:pk>/edit/', views.UserProfileUpdateView.as_view(), name='userprofile_edit'),
    path('search/', views.search_userprofile, name='search_userprofile'),
    path('search/<int:pk>/', views.search_userprofile, name='search_userprofile_with_pk'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
]