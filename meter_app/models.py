from django.db import models

# Create your models here.


class CurrentReadings(models.Model):
    voltage = models.FloatField()
    current = models.FloatField()
    power = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Only keep one row at a time
        if CurrentReadings.objects.exists():
            CurrentReadings.objects.all().delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.voltage}V | {self.current}A | {self.power}W"
