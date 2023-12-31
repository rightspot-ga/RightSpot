from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('compare/', views.compare, name='compare'),
  path('locations/starred/', views.locations_index, name='locations_index'),
  path('save_location/', views.save_location, name='save_location'),
  path('locations/<int:location_id>/', views.saved_location_detail, name='saved_location_detail'),
  path('locations/', views.location_detail, name='location_detail'),
  path('location/<int:pk>/update/', views.LocationUpdate.as_view(), name='location_update'),
  path('location/<int:pk>/delete/', views.LocationDelete.as_view(), name='location_delete'),
  path('projects/', views.projects_index, name='projects'),
  path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
  path('project/create/', views.create_project, name='create_project'),
  path('project/<int:pk>/update/', views.ProjectUpdate.as_view(), name='project_update'),
  path('project/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project_delete'),
  path('accounts/signup/', views.signup, name='signup'),
  path('faq/', views.faq, name='faq'),
  path('privacy/', views.privacy, name='privacy'),
  path('terms/', views.terms, name='terms'),
  path('settings/', views.settings, name='settings'),
  path('update_project_notes/', views.update_project_notes, name='update_project_notes'),
]