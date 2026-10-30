from django.urls import path
from . import views

app_name = 'gatepass'

urlpatterns = [
    path('', views.gatepass_list, name='list'),
    path('request/', views.request_pass, name='request'),
    path('<int:pk>/review/', views.approve_pass, name='approve'),
]