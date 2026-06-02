from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone

from .models import Club, ClubCategory, Membership, Announcement
from .forms import ClubForm, AnnouncementForm, MembershipRequestForm, RejectionForm
from notifications.models import notify


def club_list(request):
    clubs = Club.objects.filter(status='approved', is_public=True).select_related(
        'category', 'created_by'
    ).annotate(member_count_ann=Count('memberships', filter=Q(memberships__status='approved')))

    q = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', 'featured')

    if q:
        clubs = clubs.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(tags__icontains=q)
        )
    if category_slug:
        clubs = clubs.filter(category__slug=category_slug)

    if sort == 'newest':
        clubs = clubs.order_by('-created_at')
    elif sort == 'members':
        clubs = clubs.order_by('-member_count_ann')
    elif sort == 'name':
        clubs = clubs.order_by('name')
    else:
        clubs = clubs.order_by('-is_featured', '-created_at')

    categories = ClubCategory.objects.annotate(
        club_count=Count('clubs', filter=Q(clubs__status='approved'))
    ).filter(club_count__gt=0)

    user_memberships = {}
    if request.user.is_authenticated:
        for m in Membership.objects.filter(user=request.user, club__in=clubs):
            user_memberships[m.club_id] = m

    return render(request, 'clubs/list.html', {
        'clubs': clubs,
        'categories': categories,
        'q': q,
        'current_category': category_slug,
        'sort': sort,
        'user_memberships': user_memberships,
        'total_clubs': Club.objects.filter(status='approved').count(),
    })


def club_detail(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if club.status != 'approved' and not (
        request.user.is_authenticated and (
            request.user.is_platform_admin or
            club.memberships.filter(user=request.user, role__in=['owner', 'manager']).exists()
        )
    ):
        messages.error(request, "Ce club n'est pas disponible.")
        return redirect('club_list')

    membership = None
    if request.user.is_authenticated:
        membership = Membership.objects.filter(user=request.user, club=club).first()

    members = club.memberships.filter(status='approved').select_related('user').order_by(
        'role', 'joined_at'
    )[:12]
    upcoming_events = club.events.filter(
        status='published', date__gte=timezone.now().date()
    ).order_by('date')[:4]
    announcements = club.announcements.all()[:5]

    return render(request, 'clubs/detail.html', {
        'club': club,
        'membership': membership,
        'members': members,
        'upcoming_events': upcoming_events,
        'announcements': announcements,
        'can_manage': membership and membership.can_manage if membership else False,
    })


@login_required
def club_create(request):
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)
            club.created_by = request.user
            club.status = 'pending'
            club.save()
            Membership.objects.create(
                user=request.user,
                club=club,
                role='owner',
                status='approved',
                joined_at=timezone.now(),
            )
            for admin in _get_admins():
                notify(
                    admin,
                    'join_request',
                    f'Nouveau club en attente : {club.name}',
                    f'{request.user.get_full_name()} a soumis le club "{club.name}" pour validation.',
                    link=f'/admin-clubs/{club.pk}/review/',
                )
            messages.success(
                request,
                f'Le club "{club.name}" a été soumis et est en attente de validation.'
            )
            return redirect('club_detail', slug=club.slug)
    else:
        form = ClubForm()

    return render(request, 'clubs/create.html', {'form': form})


@login_required
def club_edit(request, slug):
    club = get_object_or_404(Club, slug=slug)
    _require_club_manager(request, club)

    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, 'Club mis à jour avec succès.')
            return redirect('club_detail', slug=club.slug)
    else:
        form = ClubForm(instance=club)

    return render(request, 'clubs/edit.html', {'form': form, 'club': club})


@login_required
def club_manage(request, slug):
    club = get_object_or_404(Club, slug=slug)
    _require_club_manager(request, club)

    pending = Membership.objects.filter(club=club, status='pending').select_related('user')
    members = Membership.objects.filter(club=club, status='approved').select_related('user')
    announcements = club.announcements.all()[:10]

    return render(request, 'clubs/manage.html', {
        'club': club,
        'pending_members': pending,
        'members': members,
        'announcements': announcements,
    })


@login_required
def join_club(request, slug):
    club = get_object_or_404(Club, slug=slug, status='approved')
    existing = Membership.objects.filter(user=request.user, club=club).first()

    if existing:
        if existing.status == 'approved':
            messages.info(request, 'Vous êtes déjà membre de ce club.')
        elif existing.status == 'pending':
            messages.info(request, 'Votre demande est déjà en attente.')
        elif existing.status in ('rejected', 'left'):
            existing.status = 'pending'
            existing.join_message = request.POST.get('message', '')
            existing.rejection_reason = ''
            existing.joined_at = None
            existing.save()
            _notify_managers_new_request(club, request.user)
            messages.success(request, 'Votre demande a été envoyée.')
        return redirect('club_detail', slug=slug)

    if request.method == 'POST':
        form = MembershipRequestForm(request.POST)
        if form.is_valid():
            Membership.objects.create(
                user=request.user,
                club=club,
                role='member',
                status='pending',
                join_message=form.cleaned_data.get('message', ''),
            )
            _notify_managers_new_request(club, request.user)
            messages.success(request, 'Votre demande a été envoyée aux responsables du club.')
            return redirect('club_detail', slug=slug)
    else:
        form = MembershipRequestForm()

    return render(request, 'clubs/join.html', {'club': club, 'form': form})


@login_required
def leave_club(request, slug):
    club = get_object_or_404(Club, slug=slug)
    membership = get_object_or_404(Membership, user=request.user, club=club, status='approved')

    if membership.role == 'owner':
        messages.error(request, 'Le fondateur ne peut pas quitter son club.')
        return redirect('club_detail', slug=slug)

    if request.method == 'POST':
        membership.leave()
        messages.success(request, f'Vous avez quitté le club "{club.name}".')
        return redirect('club_list')

    return render(request, 'clubs/leave_confirm.html', {'club': club})


@login_required
def approve_member(request, slug, membership_id):
    club = get_object_or_404(Club, slug=slug)
    _require_club_manager(request, club)
    membership = get_object_or_404(Membership, pk=membership_id, club=club, status='pending')

    membership.approve()
    notify(
        membership.user,
        'join_approved',
        f'Votre adhésion à {club.name} est approuvée !',
        f'Bienvenue dans le club {club.name} !',
        link=f'/clubs/{slug}/',
        sender=request.user,
    )
    messages.success(request, f'{membership.user.get_full_name()} a été accepté.')
    return redirect('club_manage', slug=slug)


@login_required
def reject_member(request, slug, membership_id):
    club = get_object_or_404(Club, slug=slug)
    _require_club_manager(request, club)
    membership = get_object_or_404(Membership, pk=membership_id, club=club, status='pending')

    reason = request.POST.get('reason', '')
    membership.reject(reason=reason)
    notify(
        membership.user,
        'join_rejected',
        f'Votre demande pour {club.name} a été refusée.',
        reason or 'Votre demande n\'a pas été retenue.',
        link=f'/clubs/{slug}/',
        sender=request.user,
    )
    messages.warning(request, f'La demande de {membership.user.get_full_name()} a été refusée.')
    return redirect('club_manage', slug=slug)


@login_required
def create_announcement(request, slug):
    club = get_object_or_404(Club, slug=slug)
    _require_club_manager(request, club)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            ann = form.save(commit=False)
            ann.club = club
            ann.author = request.user
            ann.save()
            for m in club.memberships.filter(status='approved').exclude(user=request.user):
                notify(
                    m.user,
                    'new_announcement',
                    f'Annonce de {club.name}',
                    ann.title,
                    link=f'/clubs/{slug}/',
                    sender=request.user,
                )
            messages.success(request, 'Annonce publiée.')
            return redirect('club_manage', slug=slug)
    else:
        form = AnnouncementForm()

    return render(request, 'clubs/announcement_form.html', {'form': form, 'club': club})


@login_required
def delete_announcement(request, slug, ann_id):
    club = get_object_or_404(Club, slug=slug)
    _require_club_manager(request, club)
    ann = get_object_or_404(Announcement, pk=ann_id, club=club)
    if request.method == 'POST':
        ann.delete()
        messages.success(request, 'Annonce supprimée.')
    return redirect('club_manage', slug=slug)


# ── Admin views ──────────────────────────────────────────────

@login_required
def admin_clubs(request):
    if not request.user.is_platform_admin:
        return redirect('club_list')

    status_filter = request.GET.get('status', 'pending')
    clubs = Club.objects.filter(status=status_filter).select_related(
        'category', 'created_by'
    ).order_by('-created_at')

    counts = {
        'pending': Club.objects.filter(status='pending').count(),
        'approved': Club.objects.filter(status='approved').count(),
        'rejected': Club.objects.filter(status='rejected').count(),
        'suspended': Club.objects.filter(status='suspended').count(),
    }

    return render(request, 'clubs/admin_clubs.html', {
        'clubs': clubs,
        'status_filter': status_filter,
        'counts': counts,
    })


@login_required
def admin_review_club(request, pk):
    if not request.user.is_platform_admin:
        return redirect('club_list')
    club = get_object_or_404(Club, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            club.status = 'approved'
            club.rejection_reason = ''
            club.save(update_fields=['status', 'rejection_reason'])
            notify(
                club.created_by,
                'club_approved',
                f'Votre club "{club.name}" a été approuvé !',
                'Votre club est maintenant visible sur la plateforme.',
                link=f'/clubs/{club.slug}/',
                sender=request.user,
            )
            messages.success(request, f'Le club "{club.name}" est approuvé.')
        elif action == 'reject':
            reason = request.POST.get('reason', '')
            club.status = 'rejected'
            club.rejection_reason = reason
            club.save(update_fields=['status', 'rejection_reason'])
            notify(
                club.created_by,
                'club_rejected',
                f'Votre club "{club.name}" a été refusé.',
                reason or 'Votre demande de création de club n\'a pas été retenue.',
                sender=request.user,
            )
            messages.warning(request, f'Le club "{club.name}" a été refusé.')
        elif action == 'suspend':
            club.status = 'suspended'
            club.save(update_fields=['status'])
            messages.warning(request, f'Le club "{club.name}" est suspendu.')
        return redirect('admin_clubs')

    return render(request, 'clubs/admin_review.html', {'club': club})


# ── Helpers ──────────────────────────────────────────────────

def _require_club_manager(request, club):
    membership = Membership.objects.filter(user=request.user, club=club).first()
    if not request.user.is_platform_admin and not (membership and membership.can_manage):
        messages.error(request, 'Accès refusé.')
        raise PermissionError()


def _notify_managers_new_request(club, user):
    managers = club.memberships.filter(
        status='approved', role__in=['owner', 'manager']
    ).select_related('user')
    for m in managers:
        notify(
            m.user,
            'join_request',
            f'Nouvelle demande pour {club.name}',
            f'{user.get_full_name()} souhaite rejoindre le club.',
            link=f'/clubs/{club.slug}/manage/',
            sender=user,
        )


def _get_admins():
    from presences.models import Utilisateur
    return Utilisateur.objects.filter(role='admin')
