from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.room_list, name='list'),
    path('create/', views.room_create, name='create'),
    path('<int:pk>/edit/', views.room_edit, name='edit'),
    path('<int:pk>/delete/', views.room_delete, name='delete'),
]