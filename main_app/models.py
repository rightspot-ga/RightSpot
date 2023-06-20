from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.id}) 

class Location(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=400)
    what3words = models.CharField
    #! Setting as JSONFields for now as that seems like a decent way to potentially store complex info in one field
    location = models.JSONField
    stats = models.JSONField
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('location_detail', kwargs={'pk': self.id}) 

class Deck(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=400)
    items = models.JSONField
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('deck_detail', kwargs={'pk': self.id}) 

class Static(models.Model):
    year = models.IntegerField
    

