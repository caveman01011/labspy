from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'labspaces/home.html')

def lab_index(request):
    return render(request, 'labspaces/lab_index.html')