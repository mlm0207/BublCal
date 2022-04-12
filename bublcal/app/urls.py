from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.index,        name="index"),
    path('login/',              views.login,        name="login"),
    path('signup/',             views.signup,       name="signup"),
    path('logout/',             views.logout,       name="logout"),
    path('monthly/',            views.monthly,      name="monthly-view"),
    path('glance/',             views.glance,       name="glance-view"),
    path('weekly/',             views.weekly,       name="weekly-view"),
    path('bublcreate/',         views.createBubl,   name="create-bubl"),
    path('delete/<int:id>/',    views.deleteBubl,   name="delete-bubl"),
    path('modify/<int:id>/',    views.modifyBubl,   name="modify-bubl"),
    path('deadview/',           views.deadview,     name="dead-view"),
    path('kill-bubl/<int:id>/', views.killbubl,     name="kill"),
    path('restore/<int:id>/',   views.restorebubl,  name="restore-bubl"),

    path('daily/<int:month>/<int:day>/<int:year>/',  views.daily,       name="daily-view"),
    #path('week/<int:week>/<int:year>/', views.week),
    #path('month/<int:month>/<int:year>/', views.month, name="month"),
];