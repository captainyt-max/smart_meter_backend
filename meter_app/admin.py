from django.contrib import admin

# Register your models here.
from .models import CurrentReadings

@admin.register(CurrentReadings)
class CurrentReadingsAdmin(admin.ModelAdmin):
    list_display = ('voltage', 'current', 'power', 'date', 'time')  # Show these in list
