from . import views
from django.urls import path

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  # route for sets index
  path('sets/', views.sets_index, name='index'),
]
