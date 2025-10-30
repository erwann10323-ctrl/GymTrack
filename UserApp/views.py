from django.shortcuts import render
from .models import Exercises, Workouts, Attendance, Volume, UserLogin
from .forms import ExerciseLog, EditExercise, ChangeWorkout, WorkoutCompletion, LoginForm, ResetForm
from datetime import date

# Reset fucntion checks the form ResetForm and if the value is true all the data is reset (set all data in the Volume and attendance databases to their default values)
def Reset(request):
    if request.method == 'POST':
        #Settign to correct form
        form = ResetForm(request.POST)
        if form.is_valid():
            indicator = form.cleaned_data['confirm']
            #Check the value of the inidicator
            if indicator:
                #Reset databses,set all data in the Volume and attendance databases to their default values
                Attendance.objects.all().delete()
                Volume.objects.all().delete()
            else:
                #Error message if the value isn't valid
                form.add_error('confirm', 'You must confirm the reset.')
            #Rendereing the HTML page
            return render(request, 'UserApp/home.html')
    else:
        #If no data is entered into the form the fucntion runs again
        form = ResetForm()
    return render(request, 'UserApp/Reset.html', {'form': form})

#UserChange allows the user to change the value of their username and password
def UserChange(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #retreiving the data entered by the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #Retreiving value of password and username from the UserLogin database
            userInfo = UserLogin.objects.first()
            #Setting the new values
            userInfo.username = username
            userInfo.password = password
            userInfo.save()
            #Rendering the HTML page
            return render(request, 'UserApp/home.html')
    else:
        #If no data is entered into the form the fucntion runs again
        form = LoginForm()
    return render(request, 'UserApp/UserChange.html', {'form': form})

#The login fucntion checks the information entered by the user to verify their identity before login
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #Retreivng data from the LoginForm form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #Retreiving Username and Password from the UserLogin database
            usernameS = UserLogin.objects.first().username
            passwordS = UserLogin.objects.first().password
            #Verifying the entered data (does it equal the actual Password and Username)
            if usernameS == username and passwordS == password:
                return render(request, 'UserApp/home.html')
            else:
                #If no data is entered into the form the fucntion runs again
                return render(request, 'UserApp/login.html')
    return render(request, 'UserApp/login.html')

#Statistics returns the values for the attendance and the volume done over time for the Statistics page
def Statistics(request):
    #Retreiving attendance data from the Attendance data base
    total = Attendance.objects.count()
    attended = Attendance.objects.filter(attended=True).count()
    #Calculating the attendance, attended/total * 100, unless total is 0 where attendance will be 0
    if total == 0:
        attendance = 0
    else:
        attendance = (attended / total) * 100
    #Creating lists containign the volume (reps * weight) for each workout (Push, Pull and Legs) over time
    if Volume.objects.filter(day='Push').exists():
        push_volume = []
        push_date = []
        queryset = Volume.objects.filter(day='Push').values('volume')
        for entry in queryset:
            push_volume.append(entry['volume'])
        queryset = Volume.objects.filter(day='Push').values('date')
        for entry in queryset:
            push_date.append(entry['date'])
    else:
        #Giving the variables a value if no Volume data is found
        push_volume = 'empty'
        push_date = 'empty'
    if Volume.objects.filter(day='Pull').exists():
        pull_volume = []
        pull_date = []
        queryset = Volume.objects.filter(day='Pull').values('volume')
        for entry in queryset:
            pull_volume.append(entry['volume'])
        queryset = Volume.objects.filter(day='Pull').values('date')
        for entry in queryset:
            pull_date.append(entry['date'])
    else:
        #Giving the variables a value if no Volume data is found
        pull_volume = 'empty'
        pull_date = 'empty'
    if Volume.objects.filter(day='Legs').exists():
        legs_volume = []
        legs_date = [] 
        queryset = Volume.objects.filter(day='Legs').values('volume')
        for entry in queryset:
            legs_volume.append(entry['volume'])
        queryset = Volume.objects.filter(day='Legs').values('date')
        for entry in queryset:
            legs_date.append(entry['date'])
    else:
        #Giving the variables a value if no Volume data is found
        legs_volume = 'empty'
        legs_date = 'empty'
    #Rendering the HTML page and returnign the volume and attendance data
    return render(request, 'UserApp/Statistics.html', {'attendance': attendance,
                                                       'push_volume': push_volume,
                                                       'push_date': push_date,
                                                        'pull_volume': pull_volume,
                                                        'pull_date': pull_date,
                                                        'legs_volume': legs_volume,
                                                        'legs_date': legs_date
                                                       })
#Allows the user to add or remove exercises from the Push workout, or change the day the workout is on
def PushEdit(request):
    #Retreiving the exercises for the push day
    workout = Workouts.objects.get(name='Push')
    #Retreiving the day the workout occurs on
    current_day = workout.day
    #Setting up the forms
    if request.method == 'POST':
        form1 = EditExercise(request.POST)
        form2 = ChangeWorkout(request.POST)
        action = request.POST.get('action')
        #Checking to see whether the button pressed was either add or delete
        if action in ['Add', 'Delete'] and form1.is_valid():
            name = form1.cleaned_data['name']
            day = 'Push'
            #If the delete button was pressed the exercise is deleted from the database
            if action == 'Delete':
                try:
                    exercise = Exercises.objects.get(name=name, day=day)
                    if exercise.exists():
                        exercise.delete()
                    #Rendirecting to the home HTML page
                    return render(request, 'UserApp/home.html')
                #If the exercise written isn't in the database an error message is dispalyed
                except Exercises.DoesNotExist:
                    form1.add_error('name', 'not found.')
            #If the add button is pressed the exercise is added to the exercises database
            elif action == 'Add':
                #Adding the exercise to the Exercises database
                exercise = Exercises(name=name, day=day, repetitions=0, weight=0)
                exercise.save()
                #Rendirecting to the home HTML page
                return render(request, 'UserApp/home.html')
        #If neither the delete or add buttons where pressed the day the workout occurs on is changes to the newly selected one
        elif action is None and form2.is_valid():
            day = form2.cleaned_data['day']
            workout.day = day
            workout.save()
            #Rendirecting to the home HTML page
            return render(request, 'UserApp/home.html')
    else:
        form1 = EditExercise()
        form2 = ChangeWorkout(initial={'day': current_day})
        #Running the fucntion again
    return render(request,'UserApp/PushEdit.html',{'form1': form1, 'form2': form2, 'current_day': current_day})

#Allows the user to add or remove exercises from the Pull workout, or change the day the workout is on
def PullEdit(request):
    #Retreiving the exercises for the pull day
    workout = Workouts.objects.get(name='Pull')
    #Retreiving the day the workout occurs on
    current_day = workout.day
    #Setting up the forms
    if request.method == 'POST':
        form1 = EditExercise(request.POST)
        form2 = ChangeWorkout(request.POST)
        action = request.POST.get('action')
        #Checking to see whether the button pressed was either add or delete
        if action in ['Add', 'Delete'] and form1.is_valid():
            name = form1.cleaned_data['name']
            day = 'Pull'
            #If the delete button was pressed the exercise is deleted from the database
            if action == 'Delete':
                try:
                    exercise = Exercises.objects.get(name=name, day=day)
                    if exercise.exists():
                        exercise.delete()
                    #Rendirecting to the home HTML page
                    return render(request, 'UserApp/home.html')
                except Exercises.DoesNotExist:
                    form1.add_error('name', 'not found.')
            #If the add button is pressed the exercise is added to the exercises database
            elif action == 'Add':
                exercise = Exercises(name=name, day=day, repetitions=0, weight=0)
                exercise.save()
                #Rendirecting to the home HTML page
                return render(request, 'UserApp/home.html')
        #If neither the delete or add buttons where pressed the day the workout occurs on is changes to the newly selected one
        elif action is None and form2.is_valid():
            day = form2.cleaned_data['day']
            workout.day = day
            workout.save()
            #Rendirecting to the home HTML page
            return render(request, 'UserApp/home.html')
    else:
        form1 = EditExercise()
        form2 = ChangeWorkout(initial={'day': current_day})
        #Running the fucntion again
    return render(request, 'UserApp/PullEdit.html', {'form1': form1, 'form2': form2, 'current_day': current_day})

#Allows the user to add or remove exercises from the Legs workout, or change the day the workout is on
def LegsEdit(request):
    #Retreiving the exercises for the legs day
    workout = Workouts.objects.get(name='Legs')
    #Retreiving the day the workout occurs on
    current_day = workout.day
    #Setting up the forms
    if request.method == 'POST':
        form1 = EditExercise(request.POST)
        form2 = ChangeWorkout(request.POST)
        action = request.POST.get('action')
        #Checking to see whether the button pressed was either add or delete
        if action in ['Add', 'Delete'] and form1.is_valid():
            name = form1.cleaned_data['name']
            day = 'Legs'
            #If the delete button was pressed the exercise is deleted from the database
            if action == 'Delete':
                try:
                    exercise = Exercises.objects.get(name=name, day=day)
                    if exercise.exists():
                        exercise.delete()
                    #Rendirecting to the home HTML page
                    return render(request, 'UserApp/home.html')
                except Exercises.DoesNotExist:
                    form1.add_error('name', 'not found.')
            #If the add button is pressed the exercise is added to the exercises database
            elif action == 'Add':
                exercise = Exercises(name=name, day=day, repetitions=0, weight=0)
                exercise.save()
                #Rendirecting to the home HTML page
                return render(request, 'UserApp/home.html')
        #If neither the delete or add buttons where pressed the day the workout occurs on is changes to the newly selected one
        elif action is None and form2.is_valid():
            day = form2.cleaned_data['day']
            workout.day = day
            workout.save()
            #Rendirecting to the home HTML page
            return render(request, 'UserApp/home.html')
    else:
        form1 = EditExercise()
        form2 = ChangeWorkout(initial={'day': current_day})
        #Running the fucntion again
    return render(request, 'UserApp/LegsEdit.html', {'form1': form1, 'form2': form2, 'current_day': current_day})
#add_exercise function allows for an exercise with a repetition and weigth value to be added to a workout
def add_exercise(request):
    if request.method == 'POST':
        form = EditExercise(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            day = form.cleaned_data['day']
            repetitions = form.cleaned_data['repetitions']
            weight = form.cleaned_data['weight']
            exercise = Exercises(name=name, day=day, repetitions=repetitions, weight=weight)
            exercise.save()
            return render(request, 'UserApp/home.html')
    else:
        form = EditExercise()
    return render(request, 'UserApp/add_exercise.html', {'form': form})

#The Push function opens the push workout page and allows for exercise progress to be saved and workouts to be recorded
def Push(request):
    #Retreiving data from their respective databases
    exercises = Exercises.objects.filter(day='Push')
    days = Workouts.objects.filter(name='Push')
    #Setting up the forms
    if request.method == 'POST':
        form1 = ExerciseLog(request.POST)
        form2 = WorkoutCompletion(request.POST)
        #If an exercise is logged the new weight and repetition values are saved to the database
        if form1.is_valid():
            repetitions = form1.cleaned_data['repetitions']
            weight = form1.cleaned_data['weight']
            id = form1.cleaned_data.get('id')
            exercise = Exercises.objects.get(id=id)
            exercise.repetitions = repetitions
            exercise.weight = weight
            exercise.save() 
        #If the workout completye button is pressed the attendtance for that workout is recorded and the volume is calculated
        elif form2.is_valid():
            day = date.today()
            attended = True
            attendance = Attendance(day=day, attended=attended)
            attendance.save()
            volume = sum(exercise.weight * exercise.repetitions for exercise in exercises)
            volumeDone = Volume(volume=volume, date=day, day='Push')
            volumeDone.save()
            return render(request, 'UserApp/home.html')
    else:
        form1 = ExerciseLog()
        form2 = WorkoutCompletion()
    return render(request, 'UserApp/Push.html', {'exercises': exercises,'days': days, 'form1': form1, 'form2': form2})          

#The Pull function opens the pull workout page and allows for exercise progress to be saved and workouts to be recorded
def Pull(request):
    #Retreiving data from their respective databases
    exercises = Exercises.objects.filter(day='Pull')
    days = Workouts.objects.filter(name='Pull')
    #Setting up the forms
    if request.method == 'POST':
        form1 = ExerciseLog(request.POST)
        form2 = WorkoutCompletion(request.POST)
        #If an exercise is logged the new weight and repetition values are saved to the database
        if form1.is_valid():
            repetitions = form1.cleaned_data['repetitions']
            weight = form1.cleaned_data['weight']
            id = form1.cleaned_data.get('id')
            exercise = Exercises.objects.get(id=id)
            exercise.repetitions = repetitions
            exercise.weight = weight
            exercise.save()
        #If the workout completye button is pressed the attendtance for that workout is recorded and the volume is calculated
        elif form2.is_valid():
            day = date.today()
            attended = True
            attendance = Attendance(day=day, attended=attended)
            attendance.save()
            volume = sum(exercise.weight * exercise.repetitions for exercise in exercises)
            volumeDone = Volume(volume=volume, date=day, day='Pull')
            volumeDone.save()
            return render(request, 'UserApp/home.html')
    else:
        form1 = ExerciseLog()
        form2 = WorkoutCompletion()
    return render(request, 'UserApp/Pull.html', {'exercises': exercises,'days': days, 'form1': form1, 'form2': form2})

#The Legs function opens the legs workout page and allows for exercise progress to be saved and workouts to be recorded
def Legs(request):
    #Retreiving data from their respective databases
    exercises = Exercises.objects.filter(day='Legs')
    days = Workouts.objects.filter(name='Legs')
    #Setting up the forms
    if request.method == 'POST':
        form1 = ExerciseLog(request.POST)
        form2 = WorkoutCompletion(request.POST)
        #If an exercise is logged the new weight and repetition values are saved to the database
        if form1.is_valid():
            repetitions = form1.cleaned_data['repetitions']
            weight = form1.cleaned_data['weight']
            id = form1.cleaned_data.get('id')
            exercise = Exercises.objects.get(id=id)
            exercise.repetitions = repetitions
            exercise.weight = weight
            exercise.save()
        #If the workout completye button is pressed the attendtance for that workout is recorded and the volume is calculated
        elif form2.is_valid():
            day = date.today()
            attended = True
            attendance = Attendance(day=day, attended=attended)
            attendance.save()
            volume = sum(exercise.weight * exercise.repetitions for exercise in exercises)
            volumeDone = Volume(volume=volume, date=day, day='Legs')
            volumeDone.save()
            return render(request, 'UserApp/home.html')
    else:
        form1 = ExerciseLog()
        form2 = WorkoutCompletion()
    return render(request, 'UserApp/Legs.html', {'exercises': exercises,'days': days, 'form1': form1, 'form2': form2})

#home function renders the home HTML page
def home(request):
    return render(request, 'UserApp/home.html')

#track-space fucntion renders the trackspace HTML page
def track_space(request):
    return render(request, 'UserApp/track_space.html')

#statistics fucntion renders the statistics HTML page
def statistics(request):
    return render(request, 'UserApp/statistics.html')

#settings fucntion renders the settings HTML page
def settings(request):
    return render(request, 'UserApp/settings.html')
