from . import views
from django.urls import path

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('search/', views.search, name='search'),
  # route for sets index
  path('sets/create/', views.SetCreate.as_view(), name='sets_create'),
  path('sets/<str:set_num>/', views.sets_detail, name='detail'),
  path('sets/<str:pk>/update/', views.SetUpdate.as_view(), name='sets_update'),
  path('sets/<str:pk>/delete/', views.SetDelete.as_view(), name='sets_delete'),
  path('sets/theme/<str:theme_name>/', views.sets_index, name='sets_index'),
  path('collections/', views.collections_index, name='collections_index'),
  path('collections/<int:collection_id>/parts/', views.collection_parts, name='collection_parts'),
  path('collections/create/', views.CollectionCreate.as_view(), name='collections_create'),
  path('collections/<int:collection_id>/', views.collections_detail, name='collections_detail'),
  path('collections/<int:collection_id>/update/<str:set_num>/', views.AddSetToCollection.as_view(), name='collections_update'),
  path('collections/<int:collection_id>/remove/<str:set_num>/', views.RemoveSetFromCollection.as_view(), name='collections_remove'),
  path('collections/<int:pk>/delete/', views.CollectionDelete.as_view(), name='collections_delete'),
  path('accounts/signup/', views.signup, name='signup'),
]
