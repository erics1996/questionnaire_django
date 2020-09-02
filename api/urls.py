from django.contrib import admin
from django.urls import path, re_path
from .apis import basic

urlpatterns = [
    path('surveys/', basic.SurveysApi.as_view()),
    re_path('survey/(?P<pk>\d+)/', basic.SurveysDetailApi.as_view())
]
