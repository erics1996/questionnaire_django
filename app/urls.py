from django.contrib import admin
from django.urls import path, re_path
from .views import backend

urlpatterns = [
    path('', backend.IndexView.as_view()),
    re_path('survey/(?P<pk>\d+)/', backend.SurveyDetailView.as_view()),
    re_path('(?P<pk>\d+)/download/', backend.DownloadView.as_view())
]