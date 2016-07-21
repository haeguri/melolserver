from main.models import Schedule
from main.serializers import ScheduleSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone

@api_view(['GET'])
def schedule_list(request):
    ahead_one_week = timezone.now() + timedelta(days=7)
    local_ahead_one_week = timezone.localtime(ahead_one_week)

    schedules = Schedule.objects.filter(date_time__lte=local_ahead_one_week)
    serializer = ScheduleSerializer(schedules, many=True, context={'request':request})

    return Response(serializer.data, status = status.HTTP_200_OK)