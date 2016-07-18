from django.db import models

class Schedule(models.Model):
    date_time = models.DateTimeField()
    event = models.CharField(max_length=50)

    def __str__(self):
        return str(self.date_time) + " " + self.event
