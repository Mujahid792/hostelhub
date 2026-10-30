from django.urls import path
from . import views

app_name = 'allocations'

urlpatterns = [
    path('', views.allocation_list, name='list'),
    path('allocate/', views.allocate_view, name='allocate'),
    path('<int:pk>/vacate/', views.vacate_view, name='vacate'),
]