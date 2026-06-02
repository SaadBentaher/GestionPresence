from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone

from .models import Event, EventRegistration
from .forms import EventForm
from clubs.models import Club, Membership
from notifications.models import notify


def event_list(request):
    events = Event.objects.filter(status='published').select_related(
        'club', 'club__category', 'created_by'
    ).annotate(reg_count=Count('registrations', filter=Q(registrations__status='registered')))

    q = request.GET.get('q', '').strip()
    event_type = request.GET.get('type', '').strip()
    timeframe = request.GET.get('when', 'upcoming')

    if q:
        events = events.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q)
        )
    if event_type:
        events = events.filter(event_type=event_type)

    today = timezone.now().date()
    if timeframe == 'past':
        events = events.filter(date__lt=today).order_by('-date')
    else:
        events = events.filter(date__gte=today).order_by('date', 'start_time')

    user_regs = {}
    if request.user.is_authenticated:
        for r in EventRegistration.objects.filter(user=request.user, event__in=events):
            user_regs[r.event_id] = r

    return render(request, 'events/list.html', {
        'events': events,
        'q': q,
        'event_type': event_type,
        'timeframe': timeframe,
        'user_regs': user_regs,
    })


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.status != 'published' and not (
        request.user.is_authenticated and (
            request.user.is_platform_admin or
            event.created_by == request.user
        )
    ):
        messages.error(request, "Cet événement n'est pas disponible.")
        return redirect('event_list')

    registration = None
    can_register = False
    if request.user.is_authenticated:
        registration = EventRegistration.objects.filter(
            user=request.user, event=event
        ).first()
        can_register = event.is_registration_open and not registration

    participants = event.registrations.filter(
        status='registered'
    ).select_related('user')[:20]

    return render(request, 'events/detail.html', {
        'event': event,
        'registration': registration,
        'can_register': can_register,
        'participants': participants,
        'reg_count': event.registrations.filter(status='registered').count(),
    })


@login_required
def event_create(request, club_slug):
    club = get_object_or_404(Club, slug=club_slug, status='approved')
    membership = Membership.objects.filter(user=request.user, club=club).first()

    if not request.user.is_platform_admin and not (membership and membership.can_manage):
        messages.error(request, 'Seuls les responsables du club peuvent créer des événements.')
        return redirect('club_detail', slug=club_slug)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = club
            event.created_by = request.user
            event.save()

            if event.status == 'published':
                for m in club.memberships.filter(status='approved').exclude(user=request.user):
                    notify(
                        m.user,
                        'new_event',
                        f'Nouvel événement : {event.title}',
                        f'Le club {club.name} organise "{event.title}" le {event.date}.',
                        link=f'/events/{event.pk}/',
                        sender=request.user,
                    )

            messages.success(request, f'Événement "{event.title}" créé.')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()

    return render(request, 'events/create.html', {'form': form, 'club': club})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    club = event.club
    membership = Membership.objects.filter(user=request.user, club=club).first()

    if not request.user.is_platform_admin and not (membership and membership.can_manage):
        messages.error(request, 'Accès refusé.')
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Événement mis à jour.')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit.html', {'form': form, 'event': event})


@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk, status='published')

    if not event.is_registration_open:
        messages.error(request, 'Les inscriptions sont fermées pour cet événement.')
        return redirect('event_detail', pk=pk)

    existing = EventRegistration.objects.filter(user=request.user, event=event).first()
    if existing:
        if existing.status == 'cancelled':
            existing.status = 'registered'
            existing.save(update_fields=['status'])
            messages.success(request, 'Vous êtes ré-inscrit à cet événement.')
        else:
            messages.info(request, 'Vous êtes déjà inscrit.')
        return redirect('event_detail', pk=pk)

    EventRegistration.objects.create(user=request.user, event=event, status='registered')
    messages.success(request, f'Inscription confirmée pour "{event.title}".')
    return redirect('event_detail', pk=pk)


@login_required
def event_cancel_registration(request, pk):
    event = get_object_or_404(Event, pk=pk)
    reg = get_object_or_404(EventRegistration, user=request.user, event=event)

    if request.method == 'POST':
        reg.status = 'cancelled'
        reg.save(update_fields=['status'])
        messages.success(request, 'Votre inscription a été annulée.')
        return redirect('event_detail', pk=pk)

    return render(request, 'events/cancel_confirm.html', {'event': event})
