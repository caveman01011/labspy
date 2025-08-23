from django.urls import path
from django.views.decorators.http import require_POST
from . import views

app_name = 'labspaces'

urlpatterns = [
    path('', views.home, name='home'),
    path('create_lab/', views.lab_create, name='lab_create'),
    path('lab/<str:code>/', views.labspace_view, name='labspace_view'),
    path('lab/<str:code>/pending_requests/', views.pending_requests, name='pending_requests'),

    #POST routes
    path('lab/<str:code>/accept_request/', views.accept_request, name='accept_request'),
    path('lab/<str:code>/reject_request/', views.reject_request, name='reject_request'),
]