from django.urls import path
from . import views

urlpatterns = [
    path('ons/', views.ons, name='ons'), # /api/data/ons
]