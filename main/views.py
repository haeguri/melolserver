from rest_framework import views
from main.models import Schedule, Platform, Music, Photo
from main.serializers import ScheduleSerializer, PlatformSerializer, FavorPlatformSerializer, MusicSerializer, PhotoSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper

class MelolResponse(Response):
    def __init__(self, data=None, status=None):
        super(MelolResponse, self).__init__(data, status=status)
        self.data = {'result': data}

@api_view(['GET', 'POST', 'PUT'])
def schedule_list(request):
    # ahead_one_week = timezone.now() + timedelta(days=7)
    # local_ahead_one_week = timezone.localtime(ahead_one_week)
    # schedules = Schedule.objects.filter(date_time__gte=timezone.localtime(timezone.now()), date_time__lte=local_ahead_one_week)
    # 테스트용
    if request.method == 'GET':
        schedules = Schedule.objects.all().order_by('end_date')

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

    # elif request.method == 'DELETE':
    #     try:
    #         schedule = Schedule.objects.get(id=request.data['id'])
    #     except:
    #         print("No exist schedule.")
    #         return MelolResponse("", status=status.HTTP_404_NOT_FOUND)
    #
    #     schedule.delete()
    #     schedules = Schedule.objects.all()
    #     serializer = ScheduleSerializer(schedules, many=True, context={'request':request})
    #
    #     return MelolResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def schedule_delete(request):
    if request.method == 'POST':
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
    if request.method == 'GET':
        if 'line' in request.query_params:
            platforms = Platform.objects.filter(line=request.query_params['line'])
        else:
            platforms = Platform.objects.all()

        serializer = PlatformSerializer(platforms, many=True, context={'request':request})

        return MelolResponse(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def platform_favorites(request):
    if request.method == 'GET':
        favor_platforms = Platform.objects.filter(is_favorite=True)
        serializer = FavorPlatformSerializer(favor_platforms, many=True, context={'request':request})

        return MelolResponse(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        print("before", len(Platform.objects.filter(is_favorite=True)))
        p = Platform.objects.get(id=request.data['id'])
        p.is_favorite = not p.is_favorite
        p.save()
        print("after", len(Platform.objects.filter(is_favorite=True)))

        return MelolResponse(status=status.HTTP_201_CREATED)

music_cursor = 0
@api_view(['GET', 'POST'])
def music(request):
    print("Music ..")
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

    elif request.method == 'POST':
        file = request.data['file']
        # filename = request.data['filename']

        music = Music.objects.create(file=request.data['file'])

        print(music)
        # print("File Name is", type(filename))
        # print("File is", type(file))

        return MelolResponse(status=status.HTTP_200_OK)

page_getter = lambda x: ((x-1)*9, (x-1)*9+9)

# @api_view(['GET'])
# def photo(request):
#     if request.method == 'GET':
#         if 'page' not in request.query_params:
#             photos = Photo.objects.all()
#         else:
#             page = request.query_params['page']
#             f, t = page_getter(int(page))
#             all_photos = Photo.objects.all()
#             # next_page =
#             photos = all_photos[f:t]
#
#         print(len(photos))
#
#         serializer = PhotoSerializer(photos, many=True, context={'request':request})
#
#         return Response({'result':serializer.data, 'last_page':last_page, 'first_page':first_page}, status=status.HTTP_200_OK)