from django.contrib import admin
from django.urls import path
from .apis import basic

urlpatterns = [
    path('surveys/', basic.SurveysApi.as_view())
]
