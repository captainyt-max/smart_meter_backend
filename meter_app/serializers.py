from rest_framework import serializers
from . import models

class currentReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CurrentReadings
        fields = '__all__'