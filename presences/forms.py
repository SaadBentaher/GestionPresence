from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur, Module, Seance


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = UserCreationForm.Meta.fields + ('role', 'first_name', 'last_name', 'cne', 'filiere')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['module', 'date', 'heure']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'module': forms.Select(attrs={'class': 'form-control'}),
        }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['code', 'intitule', 'filiere']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: INFO301'}),
            'intitule': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Intitulé du module'}),
            'filiere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: IRID3'}),
        }
