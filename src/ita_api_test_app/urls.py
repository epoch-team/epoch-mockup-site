from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('index', views.index),
    path('form', views.form),
    path('editRestApi', views.editRestApi),
]
