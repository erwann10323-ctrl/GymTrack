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
    #The fields of the Exercises model are defined below:
    #Name field with a CharField data type and a maximum length of 100 characters
    name = models.CharField(max_length=100)
    #Day field with a CharField data type and a maximum length of 20 characters
    day = models.CharField(max_length=20)
    #Repetitions field with a IntergerField data type
    repetitions = models.IntegerField()
    #Weight field with a FloatField data type
    weight = models.FloatField()

    def __str__(self):
        return self.name

class Workouts(models.Model):
    #The fields of the Workouts model are defined below:
    #Day field with a CharField data type and a maximum length of 20 characters
    day = models.CharField(max_length=20)
    #Name field with a CharField data type and a maximum length of 20 characters
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} workout on {self.day}"
    
class Attendance(models.Model):
    day = models.DateField()
    attended = models.BooleanField(default=False)

class Volume(models.Model):
    #The fields of the Volume model are defined below:
    #Volume field with a FloatField data type
    volume = models.FloatField()
    #Date field with a DateField data type
    date = models.DateField()
    #Day field with a CharField data type and a maximum length of 20 characters
    day = models.CharField(max_length=20)

    def __str__(self):
        return f"Volume on {self.date}: {self.volume}"
