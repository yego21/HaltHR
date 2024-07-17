from django.shortcuts import render
from django.contrib.auth.models import User

def index(request):
    users = User.objects.all()
    return render(request, 'index.html', {'users': users})