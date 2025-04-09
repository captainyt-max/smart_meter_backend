from django.core.management.base import BaseCommand
from meter_app.models import HourlyUsage

class Command(BaseCommand):
    help = 'Reset hourly usage every midnight'

    def handle(self, *args, **kwargs):
        HourlyUsage.objects.all().update(usage=0.0)
        self.stdout.write(self.style.SUCCESS('Hourly usage reset successfully!'))
