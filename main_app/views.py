from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Project, Location, Deck, Static
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def faq(request):
  return render(request, 'faq.html')

def legal(request):
  return render(request, 'legal.html')

def compare(request):
  return render(request, 'compare.html')

@login_required
def location_index(request):
  locations = 'Placeholder'
  return render(request, 'locations/index.html', {
    'locations': locations
  })

@login_required
def locations_detail(request, location_id):
  location = 'Placeholder'
  return render(request, 'location/detail.html', {
    'location': location
  })

class LocationCreate(LoginRequiredMixin, CreateView):
  model = Location
  fields = ['name', 'description']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class LocationUpdate(LoginRequiredMixin, UpdateView):
  model = Location
  fields = ['name', 'description']

class LocationDelete(LoginRequiredMixin, DeleteView):
  model = Location
  success_url = '/locations'

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
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)