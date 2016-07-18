from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^schedules/$', views.schedule_list, name='schedule_list'),
]