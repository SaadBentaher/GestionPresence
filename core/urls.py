from django.contrib import admin
from django.urls import path, include
from presences import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),

    # Admin
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/admin/users/', views.admin_users, name='admin_users'),
    path('dashboard/admin/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('dashboard/admin/modules/', views.admin_modules, name='admin_modules'),
    path('dashboard/admin/modules/<int:module_id>/delete/', views.delete_module, name='delete_module'),

    # Enseignant
    path('dashboard/enseignant/', views.dashboard_enseignant, name='dashboard_enseignant'),
    path('dashboard/enseignant/seance/<int:seance_id>/', views.mark_attendance, name='mark_attendance'),
    path('dashboard/enseignant/seance/<int:seance_id>/delete/', views.delete_seance, name='delete_seance'),
    path('dashboard/enseignant/seance/<int:seance_id>/export/', views.export_attendance_csv, name='export_attendance_csv'),

    # Etudiant
    path('dashboard/etudiant/', views.dashboard_etudiant, name='dashboard_etudiant'),
]
