from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .forms import UserRegistrationForm

# Create your views here.

def non_authenticated(request):
    return render(request, 'users/non_authenticated.html')

def login(request):
    return render(request, 'registration/login.html')

@login_required(login_url='users:login')
def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
