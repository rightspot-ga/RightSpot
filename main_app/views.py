from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Project, Location, StaticOnsData
from .forms import CustomUserCreationForm, EditUserForm, CustomPasswordChangeForm, ProjectUpdateForm, LocationUpdateForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_GET
from django.core.serializers import serialize
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from .static_data.lookups import inverse_names, comparison_variables, places_icon_lookup, types_not_needed
from .filtering import demographics_final_order_list, socioeconomics_final_order_list, industry_final_order_list
from location_services.geodetails import check_uk_district
from .helpers import fetch_from_api, get_api_base_url, format_value_as_integer_or_dash
import json
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

#! Locations 
@login_required
def locations_index(request):
		user_locations = Location.objects.filter(user=request.user).order_by('-id')
		return render(request, 'locations/index.html', {'user_locations': user_locations,'google_api_key': env('GOOGLE_MAPS_API_KEY'),})
		

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
	nearbyplaces_params = {'lat': lat, 'lng': lon, 'radius': 1000}
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
								formatted_value = format_value_as_integer_or_dash(value)
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
	
	return render(request, 'locations/detail.html', {
					'name': f"{location['address']['postcode']}, {location['address']['country']}",
					'stats': stats,
					'names': inverse_names,
					'demographics': demographics_final_order_list,
					'socioeconomics': socioeconomics_final_order_list,
					'industry': industry_final_order_list,
					'nearby': tallyPlaces(nearbyplaces),
					'location': location,
					'projects': Project.objects.filter(user=request.user) if isinstance(request.user, User) else None,
					'google_api_key': env('GOOGLE_MAPS_API_KEY'),
	})

@login_required
def save_location(request):
	if request.method == 'POST':
		location_id = request.POST.get('location_id')
		name = request.POST.get('name')
		description = request.POST.get('description')
		user = request.user
		project_ids = request.POST.getlist('projects')

		location_info = request.POST.get('location-info')
		star_location_info = request.POST.get('star-location-info')

		if location_info:
			location = json.loads(location_info)
		elif star_location_info:
			location = json.loads(star_location_info)

		if not name:
			name = f"{location['address']['postcode']}, {location['address']['country']}"

		if location_id:
			existing_location = Location.objects.get(id=location_id)
			if name: existing_location.name = name
			if description: existing_location
			if project_ids:
				for project_id in project_ids:
					existing_location.projects.add(project_id)
			existing_location.save()       
			return redirect('projects') 
		
		else:
			new_location = Location(name=name, user=user, location=location)

			if description:
				new_location.description = description

			new_location.save()

			if project_ids:
				for project_id in project_ids:
					new_location.projects.add(project_id)
			if project_ids:
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
      for year_data in stats['data']:
            for variable, value in year_data.items():
                formatted_value = format_value_as_integer_or_dash(value)
                year_data[variable] = formatted_value
  user_projects = Project.objects.filter(user=request.user)
  return render(request, 'locations/detail.html', {
      'name': saved_location.name,
      'stats': stats,
      'names': inverse_names,
      'demographics': demographics_final_order_list,
      'socioeconomics': socioeconomics_final_order_list,
      'industry': industry_final_order_list,
      'nearby': tallyPlaces(nearbyplaces),
      'location': location,
      'projects': user_projects,
      'saved': saved_location,
      'google_api_key': env('GOOGLE_MAPS_API_KEY'),
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
    form_class = LocationUpdateForm
    def get_form_kwargs(self):
        kwargs = super(LocationUpdate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        projects = form.cleaned_data.get('projects', [])
        self.object.projects.set(projects)
        self.object.save()
        next_url = self.request.GET.get('next')
        return redirect(next_url) if next_url else redirect('saved_location_detail', location_id=self.object.id)

class LocationDelete(LoginRequiredMixin, DeleteView):
    model = Location
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return redirect(next_url) if next_url else '/locations/starred'

#! Projects
@login_required
def projects_index(request):
	user_projects = Project.objects.filter(user=request.user).order_by('id')
	locations = Location.objects.filter(user=request.user)

	for project in user_projects:
		project.locations = Location.objects.filter(projects=project.id)
	
	return render(request, 'projects/index.html', {
		'user_projects': user_projects,
		'google_api_key': env('GOOGLE_MAPS_API_KEY'),
		'user_locations': locations
	})

@login_required
def project_detail(request, project_id):
	project = Project.objects.get(id=project_id)
	project.locations = Location.objects.filter(projects=project_id)
	return render(request, 'projects/detail.html', {
		'project': project,
		'google_api_key': env('GOOGLE_MAPS_API_KEY'),
	})

@login_required
def create_project(request):
		if request.method == 'POST':
				# Retrieve form data
				name = request.POST.get('name')
				description = request.POST.get('description')
				location_ids = request.POST.getlist('locations')
				user = request.user
				
				project = Project(name=name, user=user)

				if description:
						project.description = description

				project.save()

				if location_ids:
					for location_id in location_ids:
							location = Location.objects.get(id=location_id)
							project.location_set.add(location)
				return redirect('project_detail', project_id=project.id)

@login_required
def update_project_notes(request):
	if request.method == 'POST':
		project_id = request.POST.get('project_id')
		notes_content = request.POST.get('notes_content')
		project = Project.objects.get(id=project_id)
		project.notes = notes_content
		project.save()
		return JsonResponse({'success': True})
	else:
		return redirect('project_detail', project_id=project.id)	
	
class ProjectUpdate(LoginRequiredMixin, UpdateView):
	model = Project
	form_class = ProjectUpdateForm

	def get_form_kwargs(self):
		kwargs = super(ProjectUpdate, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs
	def form_valid(self, form):
		response = super(ProjectUpdate, self).form_valid(form)
		form.instance.location_set.set(form.cleaned_data['locations'])
		return redirect('project_detail', project_id=self.object.id)

class ProjectDelete(LoginRequiredMixin, DeleteView):
	model = Project
	success_url = '/projects'

#! Auth 
def signup(request):
	error_message = ''
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('home')
		else:
			error_message = 'Invalid sign up - try again'
	form = CustomUserCreationForm()
	context = {'form': form, 'error_message': error_message}
	return render(request, 'registration/signup.html', context)

#! Account Settings
@login_required
def settings(request):
		user = request.user
		error_message = ''
		tab = '#profile'
		edit_user_form = EditUserForm(instance=user, prefix='edit_user')
		password_change_form = CustomPasswordChangeForm(user, prefix='password_change')

		if request.method == 'POST':
			form_id = request.POST['form_id']
			print(form_id)

			if form_id == 'profile-settings':
				edit_user_form = EditUserForm(request.POST, instance=user, prefix='edit_user')
				tab = '#profile'
				if edit_user_form.is_valid():
						edit_user_form.save()
						return render(request, 'settings.html', {
								'edit_user_form': edit_user_form,
								'password_change_form': CustomPasswordChangeForm(user, prefix='password_change'),
								'success_message': 'User details updated successfully.',
								'tab': tab
						})
				else:
					error_message = 'Invalid changes to profile - try again'
			elif form_id == 'password-settings':
				password_change_form = CustomPasswordChangeForm(user, request.POST, prefix='password_change')
				tab = '#password'
				if password_change_form.is_valid():
						password_change_form.save()
						update_session_auth_hash(request, password_change_form.user)
						return render(request, 'settings.html', {
								'edit_user_form': EditUserForm(instance=user, prefix='edit_user'),
								'password_change_form': password_change_form,
								'success_message': 'Password updated successfully.',
								'tab': tab
						})
				else:
					error_message = 'Invalid changes to password - try again'
			elif form_id == 'delete-account':
				user.delete()
				return redirect('home')
		else:
			edit_user_form = EditUserForm(instance=user, prefix='edit_user')
			password_change_form = CustomPasswordChangeForm(user, prefix='password_change')

		return render(request, 'settings.html', {
				'edit_user_form': edit_user_form,
				'password_change_form': password_change_form,
				'error_message': error_message,
				'tab': tab
		})

#! Helper functions
def tallyPlaces(nearbyplaces):
	# Tally nearby places types
	places_type_counts = {}
	for place in nearbyplaces['results']:
			if 'types' in place:
				for place_type in place['types']:
						if place_type in places_type_counts:
								places_type_counts[place_type] += 1
						else:
								places_type_counts[place_type] = 1

	# Sort places types by count
	places_type_counts = {k: v for k, v in sorted(places_type_counts.items(), key=lambda item: item[1], reverse=True)}

	# Remove types not needed 
	for type_not_needed in types_not_needed:
			if type_not_needed in places_type_counts:
					del places_type_counts[type_not_needed]

	# Add icons to places types
	places_types = []
	for place_type in places_type_counts:
			places_types.append({
					'name': place_type,
					'count': places_type_counts[place_type],
					'icon': places_icon_lookup.get(place_type, 'bi-geo-alt')
			})
	
	# Format places types
	for place_type in places_types:
		# Replace "_" with " " in place types
		place_type['name'] = place_type['name'].replace('_', ' ')
		# Capitalise place types
		place_type['name'] = place_type['name'].title()

	return places_types