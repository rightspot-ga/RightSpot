from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Project, Location, Deck, StaticOnsData
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_GET
from django.core.serializers import serialize
from django.utils.safestring import mark_safe
from .static_data.lookups import inverse_names, comparison_variables
from .filtering import demographics_final_order_list, socioeconomics_final_order_list, industry_final_order_list
from location_services.geodetails import check_uk_district
from .helpers import fetch_from_api, get_api_base_url, format_value_as_integer_if_whole_number
import json
import environ

env = environ.Env()
environ.Env.read_env()

#! API Keys
@require_GET
def apikey_w3w(request):
  return env('W3W_API_KEY')

@require_GET
def apikey_google(request):
  return env('GOOGLE_MAPS_API_KEY')

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
    user_locations = Location.objects.filter(user=request.user, project__isnull=True).order_by('id')
    return render(request, 'locations/index.html', {'user_locations': user_locations})

def location_detail(request):
  location_name = request.GET.get('gQuery') or request.GET.get('what3words_3wa')
    
  geocode_url = get_api_base_url(request) + '/location_services/geocode'
  geocode_params = {'query': location_name}
  geocode_data = fetch_from_api(geocode_url, geocode_params)
  if not geocode_data:
      return redirect('home')
    
  lat = geocode_data['lat']
  lon = geocode_data['lng']
    
  # Fetch nearby places
  nearbyplaces_url = get_api_base_url(request) + '/location_services/nearbyplaces'
  nearbyplaces_params = {'lat': lat, 'lng': lon, 'radius': 500}
  nearbyplaces = fetch_from_api(nearbyplaces_url, nearbyplaces_params)
  if not nearbyplaces:
      return redirect('home')
    
  # Fetch address details
  geodetails_url = get_api_base_url(request) + '/location_services/geodetails'
  geodetails_params = {'lat': lat, 'lng': lon}
  addressparts = fetch_from_api(geodetails_url, geodetails_params)
  if not addressparts:
      return redirect('home')
    
  # Get district name for ONS data matching
  district = check_uk_district(addressparts)
  
  stats = None
  comparison_variables_dict = {}
  if district:
      # Fetch ONS data
      ons_url = get_api_base_url(request) + '/data/ons'
      ons_params = {'query': district}
      stats = fetch_from_api(ons_url, ons_params)
      for year_data in stats['data']:
            for variable, value in year_data.items():
                formatted_value = format_value_as_integer_if_whole_number(value)
                year_data[variable] = formatted_value
      for year_data in stats['data']:
        year = year_data['date']
        comparison_variables_dict[year] = []
        for variable, value in year_data.items():
          if variable in comparison_variables:
            comparison_variables_dict[year].append({variable: value})
  location = {
      'query': geocode_params['query'],
      'coords': (lat, lon),
      'address': addressparts,
      'nearby': nearbyplaces,
      'comparison': comparison_variables_dict
  }
  user_projects = Project.objects.filter(user=request.user)  
  return render(request, 'locations/detail.html', {
      'name': f"{location['address']['postcode']}, {location['address']['country']}",
      'stats': stats,
      'names': inverse_names,
      'demographics': demographics_final_order_list,
      'socioeconomics': socioeconomics_final_order_list,
      'industry': industry_final_order_list,
      'nearby': nearbyplaces,
      'location': location,
      'projects': user_projects,
  })

@login_required
def save_location(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    description = request.POST.get('description')
    user = request.user
    project_id = request.POST.get('project')

    location_info = request.POST.get('location-info')
    star_location_info = request.POST.get('star-location-info')

    if location_info:
      location = json.loads(location_info)
    elif star_location_info:
      location = json.loads(star_location_info)

    if not name:
      name = f"{location['address']['postcode']}, {location['address']['country']}"

    new_location = Location(name=name, user=user, location=location)

    if project_id:
      project = Project.objects.get(id=project_id)
      new_location.project = project

    if description:
      new_location.description = description

    new_location.save()  
    if project_id:
      return redirect('projects')
    else:
      return redirect('locations_index')

@login_required
def saved_location_detail(request, location_id):
  saved_location = Location.objects.get(id=location_id)
  location = saved_location.location
  nearbyplaces = location['nearby']
  addressparts = location['address']
  district = check_uk_district(addressparts)
  if district:
      # Fetch ONS data
      ons_url = get_api_base_url(request) + '/data/ons'
      ons_params = {'query': district}
      stats = fetch_from_api(ons_url, ons_params)
  user_projects = Project.objects.filter(user=request.user)
  return render(request, 'locations/detail.html', {
      'name': saved_location.name,
      'stats': stats,
      'names': inverse_names,
      'demographics': demographics_final_order_list,
      'socioeconomics': socioeconomics_final_order_list,
      'industry': industry_final_order_list,
      'nearby': nearbyplaces,
      'location': location,
      'projects': user_projects,
      'saved': saved_location
  })

@login_required
def compare(request):
  locations = Location.objects.filter(user=request.user)
  locations_json = mark_safe(serialize('json', locations))
  return render(request, 'compare.html', {
    'locations': locations,
    'locations_json': locations_json,
    'variables': comparison_variables,
    'names': inverse_names, 
  })


class LocationUpdate(LoginRequiredMixin, UpdateView):
  model = Location
  fields = ['name', 'description']
  success_url = '/locations/starred'

class LocationDelete(LoginRequiredMixin, DeleteView):
  model = Location
  success_url = '/locations/starred'

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
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)