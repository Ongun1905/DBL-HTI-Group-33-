from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("index", views.index, name="index"), #You can also link with '..\' in about.html instead of 'index', but idk whats cleaner
]
