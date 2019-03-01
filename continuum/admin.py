from django.contrib import admin
from .models import Project, Presupuesto, Votes

admin.site.register(Project)
admin.site.register(Presupuesto)
admin.site.register(Votes)
