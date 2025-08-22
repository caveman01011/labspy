from django.urls import path 
from . import views

app_name = 'labspaces'

urlpatterns = [
    path('', views.home, name='home'),
    path('create_lab/', views.lab_create, name='lab_create'),
    path('lab/<str:code>/', views.labspace_view, name='labspace_view'),
    path('lab/<str:code>/pending_requests/', views.pending_requests, name='pending_requests'),
]