from .models import Schedule, Platform
from rest_framework import serializers
from django.utils import timezone

KOREA_HOLIDAY_2016 = ('8/15','9/14','9/15','9/16','10/3','10/9','12/25',)
DAEGU_METRO_DIRECTION = {
    '1':{'up':'대곡','down':'안심'},
    '2':{'up':'문양','down':'안심'},
    '3':{'up':'칠곡경대병원','down':'용지'}
}

class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ('id', 'date_time', 'event',)

class PlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = Platform
        fields = ('id', 'name', 'line', 'is_favorite',)

class FavorPlatformSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(FavorPlatformSerializer, self).to_representation(instance)

        today_md = str(timezone.localtime(timezone.now()).month) + "/" + str(timezone.localtime(timezone.now()).day)
        today = timezone.localtime(timezone.now()).weekday()

        # cur_hour = str(timezone.localtime(timezone.now()).hour)
        # cur_minute = str(timezone.localtime(timezone.now()).minute)
        cur_time = 830

        # print("month and day", today_md)

        if today_md in KOREA_HOLIDAY_2016 or today == 6:
            # print("휴일")
            time_table = eval(instance.time_table)['휴일']
        elif today == 5:
            # print("토요일")
            time_table = eval(instance.time_table)['토요일']
        else:
            # print("평일")
            time_table = eval(instance.time_table)['평일']

        # print(time_table)

        # print("cur_hour and cur_minute", cur_hour, cur_minute)

        ret_times = {'up': {'dir':'', 'times':[]}, 'down': {'dir':'', 'times':[]}}

        for key, array in time_table.items():
            for time in array:
                i_time = int(time.split(":")[0] + time.split(":")[1])
                if cur_time >= i_time:
                    continue
                if len(ret_times[key]['times']) >= 5:
                    break
                ret_times[key]['times'].append(":".join(time.split(":")[:2]))
                ret_times[key]['dir'] = DAEGU_METRO_DIRECTION[ret['line']][key]

        # print(ret_times)

        ret['time_table'] = ret_times

        return ret

    class Meta:
        model = Platform
        fields = ('id', 'name', 'line', 'is_favorite', 'time_table',)