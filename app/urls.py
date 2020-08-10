from django.contrib import admin
from django.urls import path
from .views import basic

urlpatterns = [
    path('index/', basic.IndexView.as_view()),
]
