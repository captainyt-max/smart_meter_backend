from rest_framework import serializers
from . import models

class currentReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CurrentReadings
        fields = '__all__'

class HourlyUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HourlyUsage
        fields = ['hour', 'usage', 'last_updated']

class DailyUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailyUsage
        fields = ['date', 'usage', 'last_updated']