from django.urls import path
from . import views

urlpatterns = [
    path('', views.club_list, name='club_list'),
    path('create/', views.club_create, name='club_create'),
    path('<slug:slug>/', views.club_detail, name='club_detail'),
    path('<slug:slug>/edit/', views.club_edit, name='club_edit'),
    path('<slug:slug>/manage/', views.club_manage, name='club_manage'),
    path('<slug:slug>/join/', views.join_club, name='join_club'),
    path('<slug:slug>/leave/', views.leave_club, name='leave_club'),
    path('<slug:slug>/members/<int:membership_id>/approve/', views.approve_member, name='approve_member'),
    path('<slug:slug>/members/<int:membership_id>/reject/', views.reject_member, name='reject_member'),
    path('<slug:slug>/announce/', views.create_announcement, name='create_announcement'),
    path('<slug:slug>/announce/<int:ann_id>/delete/', views.delete_announcement, name='delete_announcement'),
]
