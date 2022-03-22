from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('main/', views.main, name="main"),
    path('daily/', views.daily, name="daily-view"),
    path('weekly/', views.weekly, name="weekly-view"),
    path('bublcreate/', views.createBubl, name="createbubl"),
    path('logout/', views.logout, name="logout"),
    path('delete/<int:id>/', views.deleteBubl),
    path('modify/<int:id>/', views.modifyBubl),
];