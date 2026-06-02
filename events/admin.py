from django.contrib import admin
from .models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'club', 'date', 'start_time', 'status', 'is_featured']
    list_filter = ['status', 'event_type', 'is_featured']
    search_fields = ['title', 'description', 'club__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'registered_at']
    list_filter = ['status']
    search_fields = ['user__username', 'event__title']
    readonly_fields = ['registered_at']
