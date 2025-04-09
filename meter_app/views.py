from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CurrentReadings, HourlyUsage, DailyUsage
from .serializers import currentReadingSerializer, HourlyUsageSerializer, DailyUsageSerializer
from rest_framework import status
from datetime import date
from django.utils import timezone



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
        'created_at': reading.created_at,
        'timestamp' : reading.timestamp,
    })


@api_view(['GET'])
def update_hourly_usage_api(request):
    hour = request.query_params.get('hour')
    usage = request.query_params.get('usage')

    if hour is None or usage is None:
        return Response({'error': 'hour and usage are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        hour = int(hour)
        usage = float(usage)

        if not 0 <= hour <= 23:
            return Response({'error': 'Hour must be between 0 and 23'}, status=status.HTTP_400_BAD_REQUEST)

        obj, created = HourlyUsage.objects.get_or_create(hour=hour)
        obj.usage = usage
        obj.save()

         # 🔁 Calculate total usage for the day
        total_daily_usage = sum(h.usage for h in HourlyUsage.objects.all())

        # 📅 Update or create today's DailyUsage
        today = date.today()
        daily_obj, created = DailyUsage.objects.get_or_create(date=today)
        daily_obj.usage = total_daily_usage
        daily_obj.save()

        serializer = HourlyUsageSerializer(obj)
        return Response({
            'hourly': serializer.data,
            'total_daily_usage': total_daily_usage,
            'date': str(today)
        })

    except ValueError:
        return Response({'error': 'Invalid hour or usage format'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_today_usage(request):
    today = date.today()

    try:
        usage_obj = DailyUsage.objects.get(date=today)
        return Response({
            'date': str(usage_obj.date),
            'usage': usage_obj.usage,
            'last_updated': usage_obj.last_updated
        })
    except DailyUsage.DoesNotExist:
        return Response({
            'error': 'No usage data available for today',
            'date': str(today)
        }, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_monthly_history(request):
    today = date.today()
    current_year = today.year
    current_month = today.month

    # 🔍 Filter records for the current month
    daily_usages = DailyUsage.objects.filter(
        date__year=current_year,
        date__month=current_month,
    ).order_by('date')

    data = [
        {
            'date': usage.date,
            'usage': usage.usage,
            'last_updated': usage.last_updated
        } for usage in daily_usages
    ]

    return Response({
        'month': today.strftime('%B'),
        'year': current_year,
        'days_recorded': len(data),
        'data': data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_hourly_usage(request):
    hourly_usages = HourlyUsage.objects.all().order_by('hour')
    serializer = HourlyUsageSerializer(hourly_usages, many=True)
    return Response({
        'total_hours': len(serializer.data),
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_total_monthly_usage(request):
    today = date.today()
    current_year = today.year
    current_month = today.month

    # Filter daily usage records for the current month
    monthly_usages = DailyUsage.objects.filter(
        date__year=current_year,
        date__month=current_month
    )

    total_usage = sum(day.usage for day in monthly_usages)

    return Response({
        'month': today.strftime('%B'),
        'year': current_year,
        'total_days_recorded': monthly_usages.count(),
        'total_usage': total_usage
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def device_status(request):
    try:
        reading = CurrentReadings.objects.latest('created_at')  # Get latest update
        time_diff = timezone.now() - reading.created_at
        is_online = time_diff.total_seconds() <= 10

        return Response({
            'status': 'Online' if is_online else 'Offline',
            'last_updated': reading.created_at,
            'time_since_update_sec': round(time_diff.total_seconds(), 2)
        }, status=status.HTTP_200_OK)

    except CurrentReadings.DoesNotExist:
        return Response({'error': 'No readings found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def reset_hourly_usage(request):
    HourlyUsage.objects.all().update(usage=0.0)
    return Response({'status': 'Hourly usage reset successfully'})