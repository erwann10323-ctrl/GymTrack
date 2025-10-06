from django import forms

# Forms are the methods used to collect data from the user through the templates
# Each form has a unique name which is refered to both in the template (HTML page) it used in and the form taking data from it
# The data type of the information being collected is defined and a variable is assigned to this data
# Error messages and verfication processes are programmed into the forms to prevent faulty data entry and crashes
# Different type of data enrty are availible, for instance the days of the workout are in a drop down list style
class ResetForm(forms.Form):
    confirm = forms.BooleanField(required=True, label='Confirm Reset', help_text='Type "true" to reset the history')
    
    def clean_confirm(self):
        confirm = self.cleaned_data.get('confirm')
        if not confirm:
            raise forms.ValidationError("You must confirm the reset.")
        return confirm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

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
