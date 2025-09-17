from django import forms

class ResetForm(forms.Form):
    confirm = forms.BooleanField(required=True, label='Confirm Reset', help_text='Check this box to confirm reset of all history data.')
    
    def clean_confirm(self):
        confirm = self.cleaned_data.get('confirm')
        if not confirm:
            raise forms.ValidationError("You must confirm the reset.")
        return confirm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(label='Password')

class ExerciseLog(forms.Form):
    repetitions = forms.IntegerField(min_value=1, label='Repetitions')
    weight = forms.FloatField(min_value=0, label='Weight (kg)')
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

class EditExercise(forms.Form):
    name = forms.CharField(max_length=100, label='Exercise Name')

class ChangeWorkout(forms.Form):
    day = forms.ChoiceField(label='Day of Workout', choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')])

class WorkoutCompletion(forms.Form):
    attended = forms.BooleanField(required=False, label='Attended Workout')