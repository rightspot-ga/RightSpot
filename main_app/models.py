from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import csv

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.JSONField()
    def __str__(self):
        return self.name

class Deck(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    items = models.JSONField
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('deck_detail', kwargs={'pk': self.id}) 

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
