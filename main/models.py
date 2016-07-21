from django.db import models

LINES = (
    ('1', '1호선'),
    ('2', '2호선'),
    ('3', '3호선'),
)

class Schedule(models.Model):
    date_time = models.DateTimeField()
    event = models.CharField(max_length=50)

    def __str__(self):
        return str(self.date_time) + " " + self.event

class Platform(models.Model):
    name = models.CharField(max_length=20)
    line = models.CharField(max_length=10, choices=LINES, null=False, blank=False)
    is_favorite = models.BooleanField(default=False)
    time_table = models.TextField()

    def __str__(self):
        return self.name + "/ 즐겨찾기 등록?" + str(self.is_favorite)