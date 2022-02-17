from django.urls import path
from . import views

urlpatterns = [
    path('daily/', views.daily),
    path('main/', views.home, name='main-view'),
    path('weekly/', views.weekly, name="weekly-view")
]
