from django.urls import path
from . import views

app_name = "spy"
urlpatterns = [
    path("", views.index, name="index"),
]
