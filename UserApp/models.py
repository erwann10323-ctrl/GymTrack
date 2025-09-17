from django.db import models

# Create your models here.
class UserLogin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Exercises(models.Model):
    name = models.CharField(max_length=100)
    day = models.CharField(max_length=20)
    repetitions = models.IntegerField()
    weight = models.FloatField()

    def __str__(self):
        return self.name

class Workouts(models.Model):
    day = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} workout on {self.day}"
    
class Attendance(models.Model):
    day = models.DateField()
    attended = models.BooleanField(default=False)

class Volume(models.Model):
    volume = models.FloatField()
    date = models.DateField()
    day = models.CharField(max_length=20)

    def __str__(self):
        return f"Volume on {self.date}: {self.volume}"
