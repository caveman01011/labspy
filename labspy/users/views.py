from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout

from .forms import UserRegistrationForm

# Create your views here.

def non_authenticated(request):
    return render(request, 'users/non_authenticated.html')

def login(request):
    return render(request, 'registration/login.html')

def logout(request):
    auth_logout(request)
    return redirect('users:login')

@login_required(login_url='users:login')
def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request)
            return redirect('users:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
