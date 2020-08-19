from django.contrib import admin
from django.urls import path, re_path
from .views import basic

urlpatterns = [
    path('', basic.IndexView.as_view()),
    re_path('(?P<pk>\d+)/download/', basic.DownloadView.as_view())
]
