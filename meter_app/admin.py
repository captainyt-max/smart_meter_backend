from django.contrib import admin

# Register your models here.
from .models import CurrentReadings, HourlyUsage, DailyUsage

@admin.register(CurrentReadings)
class CurrentReadingsAdmin(admin.ModelAdmin):
    list_display = ('voltage', 'current', 'power', 'created_at', 'timestamp')  # Show these in list

@admin.register(HourlyUsage)
class HourlyUsageAdmin(admin.ModelAdmin):
    list_display = ('hour', 'usage', 'last_updated') 

@admin.register(DailyUsage)
class DailyUsageAdmin(admin.ModelAdmin):
    list_display = ('date', 'usage', 'last_updated') 
