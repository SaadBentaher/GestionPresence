from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from presences import views as pres_views
from clubs import views as clubs_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── Landing & home ──────────────────────────────────────
    path('', pres_views.home, name='home'),

    # ── Auth ────────────────────────────────────────────────
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', pres_views.register, name='register'),

    # ── Profile ─────────────────────────────────────────────
    path('profile/', pres_views.profile_view, name='profile'),
    path('profile/edit/', pres_views.profile_edit, name='profile_edit'),

    # ── Attendance (existing) ────────────────────────────────
    path('dashboard/admin/', pres_views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/admin/users/', pres_views.admin_users, name='admin_users'),
    path('dashboard/admin/users/<int:user_id>/delete/', pres_views.delete_user, name='delete_user'),
    path('dashboard/admin/modules/', pres_views.admin_modules, name='admin_modules'),
    path('dashboard/admin/modules/<int:module_id>/delete/', pres_views.delete_module, name='delete_module'),
    path('dashboard/enseignant/', pres_views.dashboard_enseignant, name='dashboard_enseignant'),
    path('dashboard/enseignant/seance/<int:seance_id>/', pres_views.mark_attendance, name='mark_attendance'),
    path('dashboard/enseignant/seance/<int:seance_id>/delete/', pres_views.delete_seance, name='delete_seance'),
    path('dashboard/enseignant/seance/<int:seance_id>/export/', pres_views.export_attendance_csv, name='export_attendance_csv'),
    path('dashboard/etudiant/', pres_views.dashboard_etudiant, name='dashboard_etudiant'),

    # ── Clubs ───────────────────────────────────────────────
    path('clubs/', include('clubs.urls')),

    # ── Admin: club review ───────────────────────────────────
    path('admin-clubs/', clubs_views.admin_clubs, name='admin_clubs'),
    path('admin-clubs/<int:pk>/review/', clubs_views.admin_review_club, name='admin_review_club'),

    # ── Events ──────────────────────────────────────────────
    path('events/', include('events.urls')),

    # ── Notifications ────────────────────────────────────────
    path('notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
