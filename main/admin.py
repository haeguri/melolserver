from django.contrib import admin
from .models import *

class PlatformAdmin(admin.ModelAdmin):
    fields = ('name', 'line', 'is_favorite')

admin.site.register(Music)
admin.site.register(Schedule)
admin.site.register(Photo)
admin.site.register(Platform, PlatformAdmin)