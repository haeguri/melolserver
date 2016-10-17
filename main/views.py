from rest_framework import views
from main.models import Schedule, Platform, Music
from main.serializers import ScheduleSerializer, PlatformSerializer, FavorPlatformSerializer, MusicSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from datetime import timedelta
from django.utils import timezone
from .csrf_exempt_session_auth import CsrfExemptSessionAuthentication
from rest_framework.authentication import BasicAuthentication
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
from wsgiref.util import FileWrapper
import json

class MelolResponse(Response):
    def __init__(self, data=None, status=None):
        super(MelolResponse, self).__init__(data, status=status)
        self.data = {'result': data}

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def schedule_list(request):
    # ahead_one_week = timezone.now() + timedelta(days=7)
    # local_ahead_one_week = timezone.localtime(ahead_one_week)
    # schedules = Schedule.objects.filter(date_time__gte=timezone.localtime(timezone.now()), date_time__lte=local_ahead_one_week)

    # 테스트용
    if request.method == 'GET':
        schedules = Schedule.objects.all()

        serializer = ScheduleSerializer(schedules, many=True, context={'request':request})

        return MelolResponse(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        Schedule.objects.create(start_date=request.data['start_date'], end_date=request.data['end_date'], event=request.data['event'])

        schedules = Schedule.objects.all()

        serializer = ScheduleSerializer(schedules, many=True, context={'request':request})

        return MelolResponse(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        schedule = Schedule.objects.get(id=request.data['id'])

        schedule.start_date = request.data['start_date']
        schedule.end_date = request.data['end_date']
        schedule.event = request.data['event']

        schedule.save()

        schedules = Schedule.objects.all()

        serializer = ScheduleSerializer(schedules, many=True, context={'request':request})

        return MelolResponse(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        try:
            schedule = Schedule.objects.get(id=request.data['id'])
        except:
            print("No exist schedule.")
            return MelolResponse("", status=status.HTTP_404_NOT_FOUND)

        schedule.delete()

        schedules = Schedule.objects.all()

        serializer = ScheduleSerializer(schedules, many=True, context={'request':request})

        return MelolResponse(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def platform_list(request):
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, many=True, context={'request':request})

    return MelolResponse(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def platform_favorites(request):
    favor_platforms = Platform.objects.filter(is_favorite=True)
    serializer = FavorPlatformSerializer(favor_platforms, many=True, context={'request':request})

    return MelolResponse(serializer.data, status=status.HTTP_200_OK)

class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser, )
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication, )

    def post(self, request, filename, format=None):
        file_obj = request.data['file']

        print("File name is", filename)
        print("File format is", format)
        print("File object is", file_obj)

        # do something stuff after uploaded file..

        return Response(status=204)

music_cursor = 0

@api_view(['GET'])
def music(request):
    if request.method == 'GET':
        if 'cursor' not in request.query_params:
            musics = Music.objects.all().order_by('-priority')

            serializer = MusicSerializer(musics, many=True, context={'request':request})

            return MelolResponse(serializer.data, status=status.HTTP_200_OK)

        else:
            cursor = request.query_params['cursor']
            music = Music.objects.get(priority = cursor)

            music_file = open(music.file.path, 'rb')
            response = StreamingHttpResponse(FileWrapper(music_file), content_type='audio/mpeg')

            return response