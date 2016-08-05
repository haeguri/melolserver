from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^schedules/$', views.schedule_list, name='schedule_list'),
    url(r'^platforms/$', views.platform_list, name='platform_list'),
    url(r'^platforms/favorites/$', views.platform_favorites, name='platform_favorites'),
    url(r'^upload/(?P<filename>[\w.]{0,256})/$', views.FileUploadView.as_view(), name='file_upload_view'),
    url(r'^music/$', views.music, name='music'),
]