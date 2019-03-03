from django.contrib import admin
from .models import Votes, Question, Choice

admin.site.register(Votes)
admin.site.register(Question)
admin.site.register(Choice)