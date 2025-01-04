from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from company.models import Company
from .models import UserProfile
from django.urls import reverse

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
        # Check for a user ID or username in the URL
        user_id = self.kwargs.get('user_id')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            return get_object_or_404(UserProfile, user=user)

        username = self.kwargs.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            return get_object_or_404(UserProfile, user=user)

        # Default to the logged-in user's profile
        return self.request.user.userprofile

def search_userprofile(request, pk=None):
    query = request.GET.get('q')  # Fetch the query from the input
    suggestions = None
    userprofile = None

    if query:
        # Fetch suggestions for the dropdown
        suggestions = UserProfile.objects.filter(user__username__icontains=query)

    if pk:
        # If a pk is provided, fetch the UserProfile instance
        userprofile = get_object_or_404(UserProfile, pk=pk)

    return render(request, 'employee/search_userprofile.html', {
        'suggestions': suggestions,
        'userprofile': userprofile,
        'query': query,
    })


def search_suggestions(request):
    search_text = request.POST.get('q')

    # look up all films that contain the text
    # exclude user films

    suggestions = UserProfile.objects.filter(user__username__icontains=search_text)
    context = {"suggestions": suggestions}
    return render(request, 'employee/search_suggestions.html', context)





class UserProfileUpdateView(UpdateView):
    model = UserProfile
    fields = ['photo']
    template_name = 'employee/userprofile_edit.html'

    success_url = reverse_lazy('userprofile')

    def get_object(self):
        # Check if 'pk' is provided in the URL
        pk = self.kwargs.get('pk')
        if pk:
            return get_object_or_404(UserProfile, pk=pk)
        # Default to the logged-in user's profile if no 'pk' is provided
        return self.request.user.userprofile

# class UserProfileUpdateView(UpdateView):
#     model = UserProfile
#     fields = ['photo', 'employment_type', 'department']  # Add relevant fields
#     template_name = 'employee/userprofile_edit.html'
#     success_url = reverse_lazy('userprofile')
#
#     def get_object(self):
#         # Check if 'pk' is provided in the URL
#         pk = self.kwargs.get('pk')
#         if pk:
#             return get_object_or_404(UserProfile, pk=pk)
#         # Default to the logged-in user's profile if no 'pk' is provided
#         return self.request.user.userprofile
#
#     def form_valid(self, form):
#         # Save the form and check if the request is HTMX
#         self.object = form.save()
#         if self.request.headers.get('HX-Request'):
#             # Render and return the updated partial template for HTMX
#             return render(self.request, 'partials/userprofile_details.html', {'userprofile': self.object})
#         # Fallback to standard behavior for non-HTMX requests
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         if self.request.headers.get('HX-Request'):
#             # Handle validation errors in HTMX
#             return JsonResponse({'error': 'Invalid data'}, status=400)
#         # Standard invalid form handling
#         return super().form_invalid(form)








class UserPasswordChangeView(PasswordChangeView):
    template_name = 'password_change_form.html'
    success_url = reverse_lazy('profile')

# def clocker_view(request):
#     if request.method == 'GET':
