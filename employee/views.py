from django.conf.global_settings import LOGIN_URL
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.http import HttpResponse
from company.models import Event
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import PasswordChangeView
from .models import UserProfile
from django.http import JsonResponse



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()



    return render(request, 'employee/login.html', {'form': form})








def logout_view(request):
    logout(request)
    if request.headers.get('HX-Request'):
        # If the request is from HTMX, return a JSON response with the redirect URL.
        return JsonResponse({"redirect": True, "redirect_url": ""})
    else:
        # For non-HTMX requests, do a standard redirect.
        return redirect('login')


class UserProfileView(DetailView):
    model = UserProfile
    template_name = 'employee/userprofile.html'
    context_object_name = 'userprofile'

    def get_object(self):
        return self.request.user.userprofile


class UserProfileUpdateView(UpdateView):
    model = UserProfile
    fields = ['user_shift', 'photo']
    template_name = 'employee/userprofile_edit.html'
    success_url = reverse_lazy('userprofile')

    def get_object(self):
        return self.request.user.userprofile


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'password_change_form.html'
    success_url = reverse_lazy('profile')

# def clocker_view(request):
#     if request.method == 'GET':
