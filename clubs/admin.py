from django.contrib import admin
from .models import ClubCategory, Club, Membership, Announcement


@admin.register(ClubCategory)
class ClubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'display_order']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order']


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'status', 'is_featured', 'created_by', 'created_at']
    list_filter = ['status', 'is_featured', 'category']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    actions = ['approve_clubs', 'reject_clubs']

    def approve_clubs(self, request, queryset):
        queryset.update(status='approved')
    approve_clubs.short_description = 'Approuver les clubs sélectionnés'

    def reject_clubs(self, request, queryset):
        queryset.update(status='rejected')
    reject_clubs.short_description = 'Rejeter les clubs sélectionnés'


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'club', 'role', 'status', 'requested_at', 'joined_at']
    list_filter = ['status', 'role']
    search_fields = ['user__username', 'club__name']
    readonly_fields = ['requested_at', 'joined_at', 'left_at']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'club', 'author', 'is_pinned', 'created_at']
    list_filter = ['is_pinned', 'club']
    search_fields = ['title', 'content']
