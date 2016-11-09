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
        Music.objects.create(file=request.data['file'])

        return MelolResponse(status=status.HTTP_200_OK)

page_to_index = lambda x: ((x-1)*9, ((x-1)*9)+9)


@api_view(['GET'])
def photo(request):
    if request.method == 'GET':
        if 'page' not in request.query_params:
            photos = Photo.objects.all()
            serializer = PhotoSerializer(photos, many=True, context={'request':request})

            return MelolResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            page = int(request.query_params['page'])
            photos_all = Photo.objects.all()

            photo_count = len(photos_all)
            page_count = photo_count // 9

            if photo_count % 9 != 0:
                page_count += 1

            if page_count < page or page < 1:
                return Response({'result':'잘못된 페이지 번호'}, status=status.HTTP_400_BAD_REQUEST)

            from_i, to_i = page_to_index(page)

            photos = photos_all[from_i:to_i]

            prev_page = page - 1

            if prev_page < 1:
                prev_page = page_count

            next_page = (page+1) % (page_count+1)

            if next_page == 0:
                next_page += 1

            serializer = PhotoSerializer(photos, many=True, context={'request':request})

            result = {
                'count':photo_count,
                'next':next_page,
                'prev':prev_page,
                'cur':serializer.data
            }

            return Response({'result':result}, status=status.HTTP_200_OK)

