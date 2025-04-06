from django.contrib import admin
from django.urls import path, include
from . import views 


urlpatterns = [
    path("", views.home, name="current values"),
    path("currentvalue/", views.get_current_reading, name="current reading"),
    path("updatevalues", views.update_current_reading, name="update current reading"),
]
