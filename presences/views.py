import csv
from django import forms as django_forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import CustomUserCreationForm, SeanceForm, ModuleForm
from .models import Utilisateur, Module, Seance, Presence


class ProfileEditForm(django_forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'email', 'bio', 'avatar',
                  'phone', 'university', 'website', 'linkedin']
        widgets = {
            'bio': django_forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, django_forms.FileInput):
                field.widget.attrs.setdefault('class', 'form-control')


def home(request):
    if request.user.is_authenticated:
        return redirect('club_list')

    from clubs.models import Club, ClubCategory
    from events.models import Event
    from django.utils import timezone as tz
    from django.db.models import Count, Q

    categories = ClubCategory.objects.annotate(
        club_count=Count('clubs', filter=Q(clubs__status='approved'))
    ).filter(club_count__gt=0)[:8]

    featured_clubs = Club.objects.filter(
        status='approved', is_featured=True
    ).select_related('category')[:6]

    upcoming_events = Event.objects.filter(
        status='published', date__gte=tz.now().date()
    ).select_related('club').order_by('date')[:5]

    stats = {
        'clubs': Club.objects.filter(status='approved').count(),
        'members': Utilisateur.objects.filter(role__in=['etudiant', 'club_manager']).count(),
        'events': Event.objects.filter(status='published').count(),
    }

    return render(request, 'home.html', {
        'categories': categories,
        'featured_clubs': featured_clubs,
        'upcoming_events': upcoming_events,
        'stats': stats,
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard_admin(request):
    if request.user.role != 'admin':
        return redirect('home')

    recent = Seance.objects.all().order_by('-date', '-heure').select_related('module', 'enseignant')[:6]
    recent_seances = []
    for s in recent:
        total = s.presences.count()
        presents = s.presences.filter(est_present=True).count()
        recent_seances.append({
            'module': s.module,
            'enseignant': s.enseignant,
            'date': s.date,
            'total': total,
            'presents': presents,
        })

    context = {
        'total_etudiants': Utilisateur.objects.filter(role='etudiant').count(),
        'total_enseignants': Utilisateur.objects.filter(role='enseignant').count(),
        'total_modules': Module.objects.count(),
        'total_seances': Seance.objects.count(),
        'recent_seances': recent_seances,
    }
    return render(request, 'presences/admin_dashboard.html', context)


@login_required
def admin_users(request):
    if request.user.role != 'admin':
        return redirect('home')
    role_filter = request.GET.get('role', '')
    users = Utilisateur.objects.exclude(is_superuser=True).order_by('role', 'last_name', 'first_name')
    if role_filter:
        users = users.filter(role=role_filter)
    return render(request, 'presences/admin_users.html', {'users': users, 'role_filter': role_filter})


@login_required
def delete_user(request, user_id):
    if request.user.role != 'admin':
        return redirect('home')
    target = get_object_or_404(Utilisateur, id=user_id)
    if request.method == 'POST' and target != request.user:
        username = target.username
        target.delete()
        messages.success(request, f"L'utilisateur « {username} » a été supprimé.")
    return redirect('admin_users')


@login_required
def admin_modules(request):
    if request.user.role != 'admin':
        return redirect('home')
    modules = Module.objects.all().order_by('filiere', 'code')
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Module ajouté avec succès.")
            return redirect('admin_modules')
    else:
        form = ModuleForm()
    return render(request, 'presences/admin_modules.html', {'modules': modules, 'form': form})


@login_required
def delete_module(request, module_id):
    if request.user.role != 'admin':
        return redirect('home')
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        code = module.code
        module.delete()
        messages.success(request, f"Le module « {code} » a été supprimé.")
    return redirect('admin_modules')


@login_required
def dashboard_enseignant(request):
    if request.user.role != 'enseignant':
        return redirect('home')

    if request.method == 'POST':
        form = SeanceForm(request.POST)
        if form.is_valid():
            seance = form.save(commit=False)
            seance.enseignant = request.user
            seance.save()
            etudiants = Utilisateur.objects.filter(role='etudiant', filiere=seance.module.filiere)
            for etudiant in etudiants:
                Presence.objects.create(seance=seance, etudiant=etudiant)
            messages.success(request, f"Séance créée. {etudiants.count()} étudiant(s) ajouté(s) à la liste de présences.")
            return redirect('dashboard_enseignant')
    else:
        form = SeanceForm()

    seances = Seance.objects.filter(enseignant=request.user).order_by('-date', '-heure').select_related('module')
    seances_data = []
    for s in seances:
        total = s.presences.count()
        present = s.presences.filter(est_present=True).count()
        seances_data.append({
            'seance': s,
            'total': total,
            'present': present,
            'taux': round((present / total * 100) if total > 0 else 0, 1),
        })

    return render(request, 'presences/enseignant_dashboard.html', {'seances_data': seances_data, 'form': form})


@login_required
def delete_seance(request, seance_id):
    if request.user.role != 'enseignant':
        return redirect('home')
    seance = get_object_or_404(Seance, id=seance_id, enseignant=request.user)
    if request.method == 'POST':
        seance.delete()
        messages.success(request, "La séance a été supprimée.")
    return redirect('dashboard_enseignant')


@login_required
def mark_attendance(request, seance_id):
    if request.user.role != 'enseignant':
        return redirect('home')
    seance = get_object_or_404(Seance, id=seance_id, enseignant=request.user)
    presences = seance.presences.all().select_related('etudiant')

    if request.method == 'POST':
        for presence in presences:
            presence.est_present = request.POST.get(f'presence_{presence.id}') == 'on'
            presence.save()
        messages.success(request, "Les présences ont été enregistrées.")
        return redirect('dashboard_enseignant')

    present_count = presences.filter(est_present=True).count()
    return render(request, 'presences/mark_attendance.html', {
        'seance': seance,
        'presences': presences,
        'present_count': present_count,
        'absent_count': presences.count() - present_count,
    })


@login_required
def export_attendance_csv(request, seance_id):
    if request.user.role != 'enseignant':
        return redirect('home')
    seance = get_object_or_404(Seance, id=seance_id, enseignant=request.user)
    presences = seance.presences.all().select_related('etudiant')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    filename = f"presences_{seance.module.code}_{seance.date}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write('﻿')  # BOM for Excel

    writer = csv.writer(response)
    writer.writerow(['Nom', 'Prénom', 'CNE', 'Filière', 'Statut'])
    for p in presences:
        writer.writerow([
            p.etudiant.last_name,
            p.etudiant.first_name,
            p.etudiant.cne or '-',
            p.etudiant.filiere or '-',
            'Présent' if p.est_present else 'Absent',
        ])
    return response


@login_required
def dashboard_etudiant(request):
    if request.user.role != 'etudiant':
        return redirect('home')
    presences = Presence.objects.filter(etudiant=request.user).select_related(
        'seance__module', 'seance__enseignant'
    ).order_by('-seance__date')

    total = presences.count()
    present = presences.filter(est_present=True).count()
    taux = round((present / total * 100) if total > 0 else 0, 1)

    modules_data = {}
    for p in presences:
        code = p.seance.module.code
        if code not in modules_data:
            modules_data[code] = {'intitule': p.seance.module.intitule, 'total': 0, 'present': 0}
        modules_data[code]['total'] += 1
        if p.est_present:
            modules_data[code]['present'] += 1

    for k in modules_data:
        t = modules_data[k]['total']
        p_cnt = modules_data[k]['present']
        modules_data[k]['taux'] = round((p_cnt / t * 100) if t > 0 else 0, 1)

    return render(request, 'presences/etudiant_dashboard.html', {
        'presences': presences,
        'taux': taux,
        'total': total,
        'present': present,
        'absent': total - present,
        'modules_data': modules_data,
    })


@login_required
def profile_view(request):
    from clubs.models import Membership
    from events.models import EventRegistration
    memberships = Membership.objects.filter(
        user=request.user, status='approved'
    ).select_related('club').order_by('-joined_at')[:8]
    upcoming_regs = EventRegistration.objects.filter(
        user=request.user, status='registered',
        event__date__gte=__import__('datetime').date.today()
    ).select_related('event', 'event__club').order_by('event__date')[:5]
    return render(request, 'accounts/profile.html', {
        'memberships': memberships,
        'upcoming_regs': upcoming_regs,
    })


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})
