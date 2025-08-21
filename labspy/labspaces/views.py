from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Lab, LabMembership
from .forms import LabCreationForm

# Create your views here.
@login_required
def home(request):
    return render(request, 'labspaces/home.html')

@login_required
def lab_index(request):
    return render(request, 'labspaces/lab_index.html')

@login_required
def lab_create(request):
    if request.method == 'POST':
        form = LabCreationForm(request.POST)
        if form.is_valid():
            form.save()
            LabMembership.objects.create(
                lab=form.instance,
                user=request.user,
                role='owner'
            )
            return redirect('labspaces:labspace_view', code=form.instance.code)
    else:
        form = LabCreationForm()
    return render(request, 'labspaces/create-labspace.html', {'form': form})

@login_required
def labspace_view(request, code):
    labspace = Lab.objects.get(code=code)   
    return render(request, 'labspaces/labspace_view.html', {'labspace': labspace})