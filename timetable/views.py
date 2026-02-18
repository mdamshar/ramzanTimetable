from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from .models import RamadanDay, SiteSettings
from .serializers import RamadanDaySerializer, SiteSettingsSerializer
import datetime


@api_view(['GET'])
@permission_classes([AllowAny])
def get_today_timetable(request):
    """Get today's Ramadan timetable based on current date."""
    today = timezone.localdate()
    try:
        day = RamadanDay.objects.get(gregorian_date=today)
        serializer = RamadanDaySerializer(day, context={'request': request})
        return Response({'found': True, 'data': serializer.data})
    except RamadanDay.DoesNotExist:
        # Return first available day as fallback
        first_day = RamadanDay.objects.first()
        if first_day:
            serializer = RamadanDaySerializer(first_day, context={'request': request})
            return Response({'found': False, 'data': serializer.data, 'message': 'No entry for today, showing first available day.'})
        return Response({'found': False, 'data': None, 'message': 'No timetable data available.'}, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_timetable(request):
    """Get full Ramadan schedule."""
    days = RamadanDay.objects.all().order_by('ramadan_day')
    serializer = RamadanDaySerializer(days, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_day_by_number(request, day_number):
    """Get timetable for a specific Ramadan day."""
    try:
        day = RamadanDay.objects.get(ramadan_day=day_number)
        serializer = RamadanDaySerializer(day, context={'request': request})
        return Response(serializer.data)
    except RamadanDay.DoesNotExist:
        return Response({'error': 'Day not found'}, status=404)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_site_settings(request):
    """Get site settings/branding."""
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
    serializer = SiteSettingsSerializer(settings_obj, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_iftar_countdown(request):
    """Get countdown to today's Iftar."""
    today = timezone.localdate()
    now = timezone.localtime()
    try:
        day = RamadanDay.objects.get(gregorian_date=today)
        iftar_dt = datetime.datetime.combine(today, day.iftar_time)
        iftar_dt = timezone.make_aware(iftar_dt)
        diff = iftar_dt - now
        if diff.total_seconds() > 0:
            hours, remainder = divmod(int(diff.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            return Response({
                'found': True,
                'iftar_time': day.iftar_time_formatted(),
                'countdown': {'hours': hours, 'minutes': minutes, 'seconds': seconds},
                'is_iftar_passed': False
            })
        else:
            return Response({
                'found': True,
                'iftar_time': day.iftar_time_formatted(),
                'countdown': None,
                'is_iftar_passed': True
            })
    except RamadanDay.DoesNotExist:
        return Response({'found': False, 'message': 'No data for today'})


class RamadanDayViewSet(viewsets.ModelViewSet):
    queryset = RamadanDay.objects.all().order_by('ramadan_day')
    serializer_class = RamadanDaySerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
