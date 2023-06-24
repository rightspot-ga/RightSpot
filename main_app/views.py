from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Project, Location, Deck, StaticOnsData
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_GET
from .static_data.lookups import inverse_names
from .filtering import demographics_final_order_list, socioeconomics_final_order_list, industry_final_order_list
from location_services.geodetails import geoDetails, check_uk_district
from location_services.geocoding import geocodeGoogle, geocodeWhat3Words
from location_services.geoplaces import nearbyPlaces
import json
import requests
import re

import environ
env = environ.Env()
environ.Env.read_env()


#! Static page renders
def home(request):
  return render(request, 'home.html', {
    'w3w_api_key': env('W3W_API_KEY'),
    'google_api_key': env('GOOGLE_MAPS_API_KEY'),
  })

def about(request):
  return render(request, 'about.html')

def faq(request):
  return render(request, 'faq.html')

def legal(request):
  return render(request, 'legal.html')

def settings(request):
  return render(request, 'settings.html')

#! Locations 
@login_required
def locations_index(request):
  locations = 'Placeholder'
  return render(request, 'locations/index.html', {
    'locations': locations
  })

def location_detail(request):
  location_name = request.GET.get('gQuery') or request.GET.get('what3words_3wa')
  w3w_pattern = r'^///\w+\.\w+\.\w+$'
  if re.match(w3w_pattern, location_name):
    lat, lon = geocodeWhat3Words(location_name.replace('///',''))
  else:
    lat, lon = geocodeGoogle(location_name)
  nearbyplaces = nearbyPlaces(lat, lon, 500)  
  addressparts = geoDetails(lat, lon)
  district = check_uk_district(addressparts)
  location = {
    'coords': (lat, lon),
    'address': geoDetails(lat, lon),
    'nearby': nearbyplaces
  }
  if district:
    url = request.scheme + '://' + request.get_host() + '/api/data/ons'
    params = {'query': district}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        stats = response.json()
    else:
        stats = None
  else:
    stats = None
  return render(request, 'locations/detail.html', {
    'stats': stats,
    'names': inverse_names,
    'demographics': demographics_final_order_list,
    'socioeconomics': socioeconomics_final_order_list,
    'industry': industry_final_order_list,
    'nearby': nearbyplaces,
    'location': location
  })

@login_required
def save_location(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    description = request.POST.get('description')
    user = request.user
    location = json.loads(request.POST.get('location_info'))

    new_location = Location(name=name, description=description, user=user, location=location)
    new_location.save()
    
    return redirect('home')

@login_required
def saved_location_detail(request, location_id):
  location = 'Placeholder'
  return render(request, 'locations/detail.html', {
    'location': location
  })

@login_required
def compare(request):
  return render(request, 'compare.html')


class LocationUpdate(LoginRequiredMixin, UpdateView):
  model = Location
  fields = ['name', 'description']

class LocationDelete(LoginRequiredMixin, DeleteView):
  model = Location
  success_url = '/locations'

#! Decks 
@login_required
def decks_index(request):
  decks = 'Placeholder'
  return render(request, 'decks/index.html', {
    'decks': decks
  })

@login_required
def deck_detail(request, deck_id):
  deck = 'Placeholder'
  return render(request, 'deck/detail.html', {
    'deck': deck
  })

class DeckCreate(LoginRequiredMixin, CreateView):
  model = Deck
  fields = ['name', 'description']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class DeckUpdate(LoginRequiredMixin, UpdateView):
  model = Deck
  fields = ['name', 'description']

class DeckDelete(LoginRequiredMixin, DeleteView):
  model = Deck
  success_url = '/decks'

#! Projects
@login_required
def projects_index(request):
  projects = 'Placeholder'
  return render(request, 'projects/index.html', {
    'projects': projects
  })

@login_required
def project_detail(request, project_id):
  project = 'Placeholder'
  return render(request, 'project/detail.html', {
    'project': project
  })

class ProjectCreate(LoginRequiredMixin, CreateView):
  model = Project
  fields = ['name', 'description']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class ProjectUpdate(LoginRequiredMixin, UpdateView):
  model = Project
  fields = ['name', 'description']

class ProjectDelete(LoginRequiredMixin, DeleteView):
  model = Project
  success_url = '/projects'


#! Auth 
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('signup2', user)
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def signup2(request, user):

  login(request, user)

  return redirect('home')



#! API Keys
@require_GET
def apikey_w3w(request):
  return env('W3W_API_KEY')

@require_GET
def apikey_google(request):
  return env('GOOGLE_MAPS_API_KEY')