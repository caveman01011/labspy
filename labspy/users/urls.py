from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('home/', views.home, name='home'),
    #path('non-authenticated/', views.non_authenticated, name='non_authenticated'),
]

