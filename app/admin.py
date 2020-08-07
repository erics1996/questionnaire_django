from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Survey)
admin.site.register(models.ClassList)
admin.site.register(models.SurveyCode)
