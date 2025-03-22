from django.urls import path

from . import views

urlpatterns = [
    path("getCates/", views.getCates, name="getCates"),
    path("home/", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("myBrowse/", views.myBrowse, name="myBrowse"),
    path("rec/", views.rec, name="rec"),
    path("switchuser/", views.switchUser, name="switchUser"),
]