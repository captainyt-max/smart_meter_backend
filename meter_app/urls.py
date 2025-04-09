from django.contrib import admin
from django.urls import path, include
from . import views 


urlpatterns = [
    path("", views.home, name="current values"),
    path("currentvalue/", views.get_current_reading, name="current reading"),
    path("updatevalues", views.update_current_reading, name="update current reading"),
    path("update-hourly-usage", views.update_hourly_usage_api, name="update hourly usage"),
    path("get-today-usage/", views.get_today_usage, name="get today usage"),
    path("get-today-history/", views.get_all_hourly_usage, name="get today history"),
    path("get-monthly-history/", views.get_monthly_history, name="get monthly history"),
    path("get-monthly-usage/", views.get_total_monthly_usage, name="total monthly usage"),
    path('device-status/', views.device_status, name="device status"),
    path("reset-hourly/", views.reset_hourly_usage, name="reset hourly usage"),
]
