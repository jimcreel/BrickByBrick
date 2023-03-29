from . import views
from django.urls import path

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  # route for sets index
  path('sets/', views.sets_index, name='index'),
  path('sets/<int:set_id>/', views.sets_detail, name='detail'),
  path('sets/create/', views.SetCreate.as_view(), name='sets_create'),
  path('sets/<int:pk>/update/', views.SetUpdate.as_view(), name='sets_update'),
  path('sets/<int:pk>/delete/', views.SetDelete.as_view(), name='sets_delete'),
]
