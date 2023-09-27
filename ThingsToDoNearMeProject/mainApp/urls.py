from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('getEvents', views.getEvents, name='getEvents'),
    path("addEventForm", views.addEventForm, name="addEventForm"),
    path("postEvent/", views.postEvent, name='postEvent')
]