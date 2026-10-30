from django.urls import path
from . import views

app_name = 'dashboards'

urlpatterns = [
    path('', views.home, name='home'),
    path('student/', views.student_dashboard, name='student'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('technician/', views.technician_dashboard, name='technician'),
]