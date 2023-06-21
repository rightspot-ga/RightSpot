from django.urls import path
from . import views

urlpatterns = [
    path('geocode/', views.geocode_api, name='geocode'), # /api/location_services/geocode
]