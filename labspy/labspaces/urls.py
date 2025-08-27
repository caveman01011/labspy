from django.urls import path
from . import views

app_name = 'labspaces'

urlpatterns = [
    #POST routes
    path('join_lab/', views.lab_join, name="lab_join"),
    path('lab/accept_request/', views.accept_request, name='accept_request'),
    path('lab/reject_request/', views.reject_request, name='reject_request'),

    #Main routes
    path('', views.home, name='home'),
    path('create_lab/', views.lab_create, name='lab_create'),
    path('lab/<str:code>/', views.labspace_view, name='labspace_view'),
    path('lab/<str:code>/pending_requests/', views.pending_requests, name='pending_requests'),
]