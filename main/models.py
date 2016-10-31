from django.db import models
from django.utils import timezone

LINES = (
    ('1', '1호선'),
    ('2', '2호선'),
    ('3', '3호선'),
)
from time import time

def get_photo_upload_path(instance, filename):
    print("created is ", instance.created)
    # print()
    return "photos/" + timezone.localtime(timezone.now()).strftime("%y-%m-%d") + "/" + str(time()) + "/" + filename

def get_music_upload_path(instance, filename):
    return "musics/" + timezone.localtime(timezone.now()).strftime("%y-%m-%d") + "/" + str(time()) + "/" + filename

class Schedule(models.Model):
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    event = models.CharField(max_length=50)

    def __str__(self):
        return self.event

class Photo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(upload_to=get_photo_upload_path)

    def __str__(self):
        return str(self.id) + ", " + self.file.name

    def delete(self, *args, **kwargs):
        try:
            self.file.delete()
        except:
            print("이미 사진이 삭제 됐습니다.")
            super(Photo, self).delete(*args, **kwargs)

class Music(models.Model):
    # title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=get_music_upload_path)
    priority = models.PositiveSmallIntegerField(verbose_name='재생 우선순위', blank=True, null=True)

    def __str__(self):
        return str(self.id) + "@" + str(self.file)

    def save(self, *args, **kwargs):
        if self.priority is None:
            self.priority = Music.objects.order_by('-id')[0].priority + 1

        super(Music, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            self.file.delete()
        except:
            print("이미 음악 파일이 삭제 됐습니다.")

            super(Music, self).delete(*args, **kwargs)


class Platform(models.Model):
    name = models.CharField(max_length=20)
    line = models.CharField(max_length=10, choices=LINES, null=False, blank=False)
    is_favorite = models.BooleanField(default=False)
    time_table = models.TextField()

    def __str__(self):
        return self.name + "/ 즐겨찾기 등록?" + str(self.is_favorite)