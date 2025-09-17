from django.shortcuts import render
from .models import Exercises, Workouts, Attendance, Volume, UserLogin
from .forms import ExerciseLog, EditExercise, ChangeWorkout, WorkoutCompletion, LoginForm, ResetForm
from datetime import date

def Reset(request):
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            indicator = form.cleaned_data['confirm']
            if indicator:
                Attendance.objects.all().delete()
                Volume.objects.all().delete()
            else:
                form.add_error('confirm', 'You must confirm the reset.')
            return render(request, 'UserApp/home.html')
    else:
        form = ResetForm()
    return render(request, 'UserApp/Reset.html', {'form': form})
def UserChange(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            userInfo = UserLogin.objects.first()
            userInfo.username = username
            userInfo.password = password
            userInfo.save()
            return render(request, 'UserApp/home.html')
    else:
        form = LoginForm()
    return render(request, 'UserApp/UserChange.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usernameS = UserLogin.objects.first().username
            passwordS = UserLogin.objects.first().password
            if usernameS == username and passwordS == password:
                return render(request, 'UserApp/home.html')
            else:
                
                return render(request, 'UserApp/login.html')
    return render(request, 'UserApp/login.html')


def Statistics(request):
    total = Attendance.objects.count()
    attended = Attendance.objects.filter(attended=True).count()
    if total == 0:
        attendance = 0
    else:
        attendance = (attended / total) * 100
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
        legs_volume = 'empty'
        legs_date = 'empty'
    return render(request, 'UserApp/Statistics.html', {'attendance': attendance,
                                                       'push_volume': push_volume,
                                                       'push_date': push_date,
                                                        'pull_volume': pull_volume,
                                                        'pull_date': pull_date,
                                                        'legs_volume': legs_volume,
                                                        'legs_date': legs_date
                                                       })

def PushEdit(request):
    workout = Workouts.objects.get(name='Push')
    current_day = workout.day

    if request.method == 'POST':
        form1 = EditExercise(request.POST)
        form2 = ChangeWorkout(request.POST)
        action = request.POST.get('action')
        if action in ['Add', 'Delete'] and form1.is_valid():
            name = form1.cleaned_data['name']
            day = 'Push'
            if action == 'Delete':
                try:
                    exercise = Exercises.objects.get(name=name, day=day)
                    exercise.delete()
                    return render(request, 'UserApp/home.html')
                except Exercises.DoesNotExist:
                    form1.add_error('name', 'not found.')
            elif action == 'Add':
                exercise = Exercises(name=name, day=day, repetitions=0, weight=0)
                exercise.save()
                return render(request, 'UserApp/home.html')
        elif action is None and form2.is_valid():
            day = form2.cleaned_data['day']
            workout.day = day
            workout.save()
            return render(request, 'UserApp/home.html')
    else:
        form1 = EditExercise()
        form2 = ChangeWorkout(initial={'day': current_day})
    return render(request,'UserApp/PushEdit.html',{'form1': form1, 'form2': form2, 'current_day': current_day})

def PullEdit(request):
    workout = Workouts.objects.get(name='Pull')
    current_day = workout.day
    if request.method == 'POST':
        form1 = EditExercise(request.POST)
        form2 = ChangeWorkout(request.POST)
        action = request.POST.get('action')
        if action in ['Add', 'Delete'] and form1.is_valid():
            name = form1.cleaned_data['name']
            day = 'Pull'
            if action == 'Delete':
                try:
                    exercise = Exercises.objects.get(name=name, day=day)
                    exercise.delete()
                    return render(request, 'UserApp/home.html')
                except Exercises.DoesNotExist:
                    form1.add_error('name', 'not found.')
            elif action == 'Add':
                exercise = Exercises(name=name, day=day, repetitions=0, weight=0)
                exercise.save()
                return render(request, 'UserApp/home.html')
        elif action is None and form2.is_valid():
            day = form2.cleaned_data['day']
            workout.day = day
            workout.save()
            return render(request, 'UserApp/home.html')
    else:
        form1 = EditExercise()
        form2 = ChangeWorkout(initial={'day': current_day})
    return render(request, 'UserApp/PullEdit.html', {'form1': form1, 'form2': form2, 'current_day': current_day})

def LegsEdit(request):
    workout = Workouts.objects.get(name='Legs')
    current_day = workout.day
    if request.method == 'POST':
        form1 = EditExercise(request.POST)
        form2 = ChangeWorkout(request.POST)
        action = request.POST.get('action')
        if action in ['Add', 'Delete'] and form1.is_valid():
            name = form1.cleaned_data['name']
            day = 'Legs'
            if action == 'Delete':
                try:
                    exercise = Exercises.objects.get(name=name, day=day)
                    exercise.delete()
                    return render(request, 'UserApp/home.html')
                except Exercises.DoesNotExist:
                    form1.add_error('name', 'not found.')
            elif action == 'Add':
                exercise = Exercises(name=name, day=day, repetitions=0, weight=0)
                exercise.save()
                return render(request, 'UserApp/home.html')
        elif action is None and form2.is_valid():
            day = form2.cleaned_data['day']
            workout.day = day
            workout.save()
            return render(request, 'UserApp/home.html')
    else:
        form1 = EditExercise()
        form2 = ChangeWorkout(initial={'day': current_day})
    return render(request, 'UserApp/LegsEdit.html', {'form1': form1, 'form2': form2, 'current_day': current_day})

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

def Push(request):
    exercises = Exercises.objects.filter(day='Push')
    days = Workouts.objects.filter(name='Push')
    if request.method == 'POST':
        form1 = ExerciseLog(request.POST)
        form2 = WorkoutCompletion(request.POST)
        if form1.is_valid():
            repetitions = form1.cleaned_data['repetitions']
            weight = form1.cleaned_data['weight']
            id = form1.cleaned_data.get('id')
            exercise = Exercises.objects.get(id=id)
            exercise.repetitions = repetitions
            exercise.weight = weight
            exercise.save() 
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

def Pull(request):
    exercises = Exercises.objects.filter(day='Pull')
    days = Workouts.objects.filter(name='Pull')
    if request.method == 'POST':
        form1 = ExerciseLog(request.POST)
        form2 = WorkoutCompletion(request.POST)
        if form1.is_valid():
            repetitions = form1.cleaned_data['repetitions']
            weight = form1.cleaned_data['weight']
            id = form1.cleaned_data.get('id')
            exercise = Exercises.objects.get(id=id)
            exercise.repetitions = repetitions
            exercise.weight = weight
            exercise.save() 
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

def Legs(request):
    exercises = Exercises.objects.filter(day='Legs')
    days = Workouts.objects.filter(name='Legs')
    if request.method == 'POST':
        form1 = ExerciseLog(request.POST)
        form2 = WorkoutCompletion(request.POST)
        if form1.is_valid():
            repetitions = form1.cleaned_data['repetitions']
            weight = form1.cleaned_data['weight']
            id = form1.cleaned_data.get('id')
            exercise = Exercises.objects.get(id=id)
            exercise.repetitions = repetitions
            exercise.weight = weight
            exercise.save() 
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

def home(request):
    return render(request, 'UserApp/home.html')
def track_space(request):
    return render(request, 'UserApp/track_space.html')
def statistics(request):
    return render(request, 'UserApp/statistics.html')
def settings(request):
    return render(request, 'UserApp/settings.html')