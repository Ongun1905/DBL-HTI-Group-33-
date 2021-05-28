from django.urls import path
from . import views
from homepage.dash_apps.finished_apps import graph_visualisation

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("vis1", views.vis1, name ="vis1"),
    path("vis2", views.vis2, name ="vis2"),
    path("vis_combined", views.vis_combined, name = "vis_combined"),
]