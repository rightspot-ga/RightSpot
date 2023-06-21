from django.contrib import admin
from .models import Project, Location, Deck, Static

# Register your models here.
admin.site.register(Project)
admin.site.register(Location)
admin.site.register(Deck)
admin.site.register(Static)