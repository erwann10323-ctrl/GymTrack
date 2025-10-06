from django.urls import path
from . import views

#The templates (HTML files) are linked to a URL extension (e.g home/) and a view (function)
urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('track/', views.track_space, name='track_space'),
    path('statistics/', views.Statistics, name='Statistics'),
    path('settings/', views.settings, name='Settings'),
    path('push/', views.Push, name='Push'),
    path('pull/', views.Pull, name='Pull'),
    path('legs/', views.Legs, name='Legs'),
    path('PushEdit/', views.PushEdit, name='PushEdit'),
    path('PullEdit/', views.PullEdit, name='PullEdit'),
    path('LegsEdit/', views.LegsEdit, name='LegsEdit'),
    path('UserChange/', views.UserChange, name='UserChange'),
    path('Reset/', views.Reset, name='Reset'),
]
