from django.contrib import admin

# Register your models here.
from .models import Exercises, Workouts, Attendance, Volume, UserLogin

admin.site.register(Exercises)
admin.site.register(Workouts)
admin.site.register(Attendance)
admin.site.register(Volume)
admin.site.register(UserLogin)