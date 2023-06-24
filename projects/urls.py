from django.urls import path
from . import views, carina, weather, crypto, quiz

urlpatterns = [
    path('', views.login, name = 'home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
    path('carina', carina.carina, name='carina'),
    path('weather', weather.weather, name='weather'),
    path('crypto', crypto.cryptic, name='crypto'),
    path('quiz', quiz.quiz, name='quiz')
    ]
