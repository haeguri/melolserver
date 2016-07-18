from .models import Schedule
from rest_framework import serializers

class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ('id', 'date_time', 'event')