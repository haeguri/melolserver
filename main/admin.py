from django.contrib import admin
from .models import Schedule, Platform

class PlatformAdmin(admin.ModelAdmin):
    fields = ('name', 'line', 'is_favorite')

admin.site.register(Schedule)
admin.site.register(Platform, PlatformAdmin)