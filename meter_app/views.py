from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CurrentReadings
from .serializers import currentReadingSerializer



# Create your views here.

def home(request):
    return HttpResponse("smart meter app home")
 

@api_view(['GET'])
def get_current_reading(request):
    reading = CurrentReadings.objects.first()
    if reading:
        serializer = currentReadingSerializer(reading)
        return Response(serializer.data)
    return Response({'message': 'No data found'})

@api_view(['GET'])
def update_current_reading(request):
    voltage = request.GET.get('voltage')
    current = request.GET.get('current')
    power = request.GET.get('power')

    if not voltage or not current or not power:
        return Response({'error': 'Missing voltage, current, or power'}, status=400)

    # Convert to float for saving
    voltage = float(voltage)
    current = float(current)
    power = float(power)

     # If row doesn't exist, create with values
    reading, created = CurrentReadings.objects.get_or_create(
        id=1,
        defaults={
            'voltage': voltage,
            'current': current,
            'power': power,
        }
    )
     # If it already existed, update it
    if not created:
        reading.voltage = voltage
        reading.current = current
        reading.power = power
        reading.save()

    return Response({
        'message': 'Data updated successfully',
        'voltage': reading.voltage,
        'current': reading.current,
        'power': reading.power,
        'date': reading.date,
        'time': reading.time,
    })
