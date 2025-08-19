from django.urls import path 
from . import views

app_name = 'labspaces'

urlpatterns = [
    path('', views.home, name='home'),
    path('lab/', views.lab_index, name='lab_index'),
]