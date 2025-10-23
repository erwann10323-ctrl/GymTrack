from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from datetime import datetime, date, timedelta
from UserApp.models import Workouts, Attendance

class Command(BaseCommand):
    help = 'Send Reminder Email'
#This fucntion sends an email to the user to either notify them on an upcoming worokout or congratulate them on a completed one, this function will be run every morning using python anywheres task schedueler
    def handle(self, *args, **options):
        now = datetime.now().strftime("%A")
        workout = Workouts.objects.filter(day = now).first()
        if workout is not None:
            send_mail(
                'Gym Tracker Reminder',
                'Workout today!',
                'erwanncreates@gmail.com',
                ['erwann10323@g.lfis.edu.hk'],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"Sent email to erwann10323"))
        yesterday = date.today() - timedelta(days=1)
        yesterday_week = yesterday.strftime("%A")
        y_workout = Workouts.objects.filter(day=yesterday_week).first()
        if y_workout is not None:
            y_attendance = Attendance.objects.filter(day=yesterday).first()
            if y_attendance is None:
                Attendance.objects.create(day=yesterday, attended=False)
                self.stdout.write(self.style.SUCCESS(f"Created attendance record for {yesterday}"))
            else:
                Attendance.objects.create(day=yesterday, attended=True)
                send_mail(
                    'Gym Tracker Reminder',
                    'Good job on your workout yesterday!',
                    'erwanncreates@gmail.com',
                    ['erwann10323@g.lfis.edu.hk'],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f"Sent email to erwann10323 for yesterday's workout"))          
