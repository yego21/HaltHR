from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from company.models import Event
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
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
    return redirect('login')

def test_view(request):
    test = 'hahahha'
    return render(request, 'index', {'test': test})

# def clocker_view(request):
#     if request.method == 'GET':
