from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^schedules/$', views.schedule_list, name='schedule_list'),
    url(r'^platforms/$', views.platform_list, name='platform_list'),
    url(r'^platforms/favorites/$', views.platform_favorites, name='platform_favorites'),
]