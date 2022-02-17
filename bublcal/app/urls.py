from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('daily/', views.daily, name="daily-view"),
    path('weekly/', views.weekly, name="weekly-view"),
];