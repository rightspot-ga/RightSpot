from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
import csv

class Project(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=400, default='No description')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(default='')
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'project_id': self.id}) 

class Location(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=400, default='No description')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project)
    location = models.JSONField()
    def __str__(self):
        return self.name

# Cleaning up relationships on deletion 
@receiver(pre_delete, sender=Location)
def remove_location_from_projects(sender, instance, **kwargs):
    instance.projects.clear()

@receiver(pre_delete, sender=Project)
def remove_project_from_locations(sender, instance, **kwargs):
    instance.location_set.clear()    

# Create Django model using .csv file headers as fields
csv_file_path = 'main_app/static_data/rightspot_wide.csv'

with open(csv_file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    headers = next(reader) 

model_fields = {}

for column_name in headers[2:]:
    model_fields[column_name] = models.DecimalField(max_digits=10, decimal_places=2) 

model_fields['district'] = models.CharField(max_length=300)
model_fields['date'] = models.IntegerField()

class Meta:
    app_label = 'main_app'

model_attrs = {
    '__module__': __name__,
    'Meta': Meta,
    **model_fields,
}

StaticOnsData = type('StaticOnsData', (models.Model,), model_attrs)
