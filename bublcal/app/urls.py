from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('main/', views.main, name="main"),
    path('daily/', views.daily, name="daily-view"),
    path('weekly/', views.weekly, name="weekly-view"),
    path("success/", views.signup_success, name="signup-success"),
];