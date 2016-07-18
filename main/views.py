from main.models import Schedule
from main.serializers import ScheduleSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def schedule_list(request):
    schedules = Schedule.objects.all()
    serializer = ScheduleSerializer(schedules, many=True, context={'request':request})

    return Response(serializer.data, status = status.HTTP_200_OK)

