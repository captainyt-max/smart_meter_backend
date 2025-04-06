from django.db import models
import time
from datetime import datetime, timedelta
from django.utils import timezone

def get_timestamp_millis():
    ist_now = timezone.localtime(timezone.now())  # returns IST if TIME_ZONE is set
    return int(ist_now.timestamp())

# Create your models here.


class CurrentReadings(models.Model):
    voltage = models.FloatField()
    current = models.FloatField()
    power = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.BigIntegerField(default=get_timestamp_millis)

    def save(self, *args, **kwargs):
        # Only keep one row at a time
        if CurrentReadings.objects.exists():
            CurrentReadings.objects.all().delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.voltage}V | {self.current}A | {self.power}W"
