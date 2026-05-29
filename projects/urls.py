from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.ProjectListView.as_view(),
         name='project_list'),
    path('<int:pk>/', views.ProjectDetailView.as_view(),
         name='project_detail'),
    path('create-project/', views.ProjectCreateView.as_view(),
         name='project_create'),
    path('<int:pk>/edit/', views.ProjectUpdateView.as_view(),
         name='project_update'),
    path('<int:pk>/complete/', views.project_complete,
         name='project_complete'),
    path('<int:pk>/toggle_participate/', views.toggle_participate,
         name='toggle_participate'),
    path('skills/', views.skill_autocomplete,
         name='skill_autocomplete'),
    path('<int:pk>/skills/add/', views.add_skill_to_project,
         name='add_skill'),
    path('<int:project_pk>/skills/<int:skill_pk>/remove/',
         views.remove_skill_from_project,
         name='remove_skill'),
]
