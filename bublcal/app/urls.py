from django.urls import path
from . import views

urlpatterns = [
    path("",                    views.index,        name="index"),

    path("login/",              views.login,        name="login"),
    path("logout/",             views.logout,       name="logout"),
    path("signup/",             views.signup,       name="signup"),

    path("glance/",             views.glance,       name="glance-view"),
    path("deadview/",           views.deadview,     name="dead-view"),

    path("bublcreate/",         views.createBubl,   name="create-bubl"),
    path("delete/<int:id>/",    views.deleteBubl,   name="delete-bubl"),
    path("modify/<int:id>/",    views.modifyBubl,   name="modify-bubl"),
    path("complete/<int:id>/",  views.complete,     name="complete-bubl"),
    path("kill-bubl/<int:id>/", views.killbubl,     name="kill-bubl"),
    path("restore/<int:id>/",   views.restorebubl,  name="restore-bubl"),

    path("profile/",            views.profile,      name="profile"),

    path("daily/<int:month>/<int:day>/<int:year>/",     views.daily,    name="daily-view"),
    path("weekly/<int:month>/<int:day>/<int:year>/",    views.weekly,   name="weekly-view"),
    path("monthly/<int:month>/<int:year>/",             views.monthly,  name="monthly-view"),
];