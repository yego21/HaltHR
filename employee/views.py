from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from company.models import Company
from .models import UserProfile


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

    company = Company.get_solo()
    hero_images = [
        company.hero_image1 if company.hero_image1 else None,
        company.hero_image2 if company.hero_image2 else None,
        company.hero_image3 if company.hero_image3 else None,
        company.hero_image4 if company.hero_image4 else None,
        company.hero_image5 if company.hero_image5 else None,
    ]
    hero_images = [image for image in hero_images if image is not None]
    context = {
        'form': form,
        'hero_images': hero_images
    }
    return render(request, 'employee/login.html', context)

    # return render(request, 'employee/login.html', {'form': form})


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
    fields = ['photo']
    template_name = 'employee/userprofile_edit.html'
    success_url = reverse_lazy('userprofile')

    def get_object(self):
        return self.request.user.userprofile


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'password_change_form.html'
    success_url = reverse_lazy('profile')

# def clocker_view(request):
#     if request.method == 'GET':
