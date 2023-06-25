from django.contrib import admin
from .models import Project, Location, StaticOnsData

# Register your models here.
admin.site.register(Project)
admin.site.register(Location)
admin.site.register(StaticOnsData)