from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Survey)
admin.site.register(models.Answer)
admin.site.register(models.QuestionOptions)
admin.site.register(models.Question)