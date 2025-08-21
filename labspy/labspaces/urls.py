from django.urls import path 
from . import views

app_name = 'labspaces'

urlpatterns = [
    path('', views.home, name='home'),
    path('create_lab/', views.lab_create, name='lab_create'),
    path('labspace/<int:code>/', views.labspace_view, name='labspace_view'),
]