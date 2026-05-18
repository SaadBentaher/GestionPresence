from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Module, Seance, Presence

class CustomUserAdmin(UserAdmin):
    model = Utilisateur
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('role', 'cne', 'filiere')}),
    )

admin.site.register(Utilisateur, CustomUserAdmin)
admin.site.register(Module)
admin.site.register(Seance)
admin.site.register(Presence)
