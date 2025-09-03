from django.urls import path
from . import views

app_name = 'labspaces'

urlpatterns = [
    #Main routes
    path('/', views.home, name='home'),
    path('user_pending_labs/', views.user_pending_labs, name="user_pending_labs"),
    path('create_lab/', views.lab_create, name='lab_create'),
    path('lab/<str:code>/', views.labspace_view, name='labspace_view'),
    path('lab/<str:code>/pending_requests/', views.pending_requests, name='pending_requests'),
    path('lab/<str:code>/manage_members/', views.manage_members, name='manage_members'),
    path('lab/<str:code>/manage_permissions/', views.manage_permissions, name='manage_permissions'),

    #POST routes
    path('join_lab/', views.lab_join, name="lab_join"),
    path('cancel_join_request/', views.cancel_join_request, name="cancel_join_request"),
    path('accept_request/', views.accept_request, name='accept_request'),
    path('reject_request/', views.reject_request, name='reject_request'),
    path('lab/<str:code>/remove_member/', views.remove_member, name='remove_member'),
]