from django.urls import path
from . import views

urlpatterns = [
    path('geocode/', views.geocode, name='geocode'), # /api/location_services/geocode
    path('geodetails/', views.location_details, name='geodetails'), # /api/location_services/geodetails
]