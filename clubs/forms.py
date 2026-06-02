from django import forms
from .models import Club, ClubCategory, Announcement


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = [
            'name', 'short_description', 'description', 'category',
            'logo', 'banner', 'founding_date', 'contact_email',
            'contact_phone', 'website', 'facebook', 'instagram',
            'twitter', 'linkedin', 'max_members', 'tags', 'is_public',
        ]
        widgets = {
            'founding_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'short_description': forms.Textarea(attrs={'rows': 2}),
            'tags': forms.TextInput(attrs={'placeholder': 'technologie, robotique, IA ...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput,
                                         forms.URLInput, forms.Select,
                                         forms.NumberInput)):
                field.widget.attrs.setdefault('class', 'form-control')
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('class', 'form-control')


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'is_pinned']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['class'] = 'form-control'


class MembershipRequestForm(forms.Form):
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Présentez-vous et expliquez pourquoi vous souhaitez rejoindre ce club...',
        }),
        label='Message de motivation (optionnel)',
    )


class RejectionForm(forms.Form):
    reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Raison du refus (optionnelle)...',
        }),
        label='Raison du refus',
    )
