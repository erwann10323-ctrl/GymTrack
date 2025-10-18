from django.db import models

# Models (databases) are created here
# The collums and their data types are defined within the definition of the model

# The model's name is defined as UserLogin to represent user credentials
class UserLogin(models.Model):
    #The fields of the UserLogin model are defined below:
    #Username field with a CharField data type and a maximum length of 100 characters
    username = models.CharField(max_length=100)
    #Password field with a CharField data type and a maximum length of 100 characters
    password = models.CharField(max_length=100)
    #Defining the method used to retreive an value of this model (returns the username)
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
