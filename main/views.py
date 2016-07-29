from rest_framework import views
from main.models import Schedule, Platform
from main.serializers import ScheduleSerializer, PlatformSerializer, FavorPlatformSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from datetime import timedelta
from django.utils import timezone
from .csrf_exempt_session_auth import CsrfExemptSessionAuthentication
# from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import BasicAuthentication

@api_view(['GET'])
def schedule_list(request):
    ahead_one_week = timezone.now() + timedelta(days=7)
    local_ahead_one_week = timezone.localtime(ahead_one_week)

    schedules = Schedule.objects.filter(date_time__gte=timezone.localtime(timezone.now()), date_time__lte=local_ahead_one_week)
    serializer = ScheduleSerializer(schedules, many=True, context={'request':request})

    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])
def platform_list(request):
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, many=True, context={'request':request})

    return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])
def platform_favorites(request):
    favor_platforms = Platform.objects.filter(is_favorite=True)
    serializer = FavorPlatformSerializer(favor_platforms, many=True, context={'request':request})

    return Response(serializer.data, status = status.HTTP_200_OK)

class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser, )
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication, )

    def post(self, request, filename, format=None):
        file_obj = request.data['file']

        print("File name is", filename)
        print("File format is", format)
        print("File object is", file_obj)

        # do something stuff with uploaded file..

        return Response(status = 204)