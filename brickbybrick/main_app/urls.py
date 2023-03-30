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
  path('collections/', views.collections_index, name='collections_index'),
  path('collections/<int:collection_id>/', views.collections_detail, name='collections_detail'),
  path('collections/<int:collection_id>/update/<int:set_id>/', views.AddSetToCollection.as_view(), name='collections_update'),
  path('collections/create/', views.CollectionCreate.as_view(), name='collections_create'),
  path('collections/<int:pk>/delete/', views.CollectionDelete.as_view(), name='collections_delete'),
]
