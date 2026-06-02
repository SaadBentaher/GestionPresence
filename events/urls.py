from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/register/', views.event_register, name='event_register'),
    path('<int:pk>/cancel/', views.event_cancel_registration, name='event_cancel_registration'),
    path('<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('create/<slug:club_slug>/', views.event_create, name='event_create'),
]
