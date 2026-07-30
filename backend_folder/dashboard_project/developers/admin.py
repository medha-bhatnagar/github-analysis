from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Profile, MetricData, FileData

admin.site.register(Profile)
admin.site.register(MetricData)
admin.site.register(FileData)