from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    path('submit/', views.submit_complaint, name='submit'),
    path('track/', views.track_complaints, name='track'),
    path('<int:pk>/assign/', views.assign_complaint, name='assign'),
    path('<int:pk>/update/', views.technician_update, name='update'),
]