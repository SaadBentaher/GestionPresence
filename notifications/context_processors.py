def notifications_context(request):
    ctx = {'unread_notif_count': 0, 'pending_clubs_count': 0}
    if request.user.is_authenticated:
        ctx['unread_notif_count'] = request.user.notifications.filter(is_read=False).count()
        if getattr(request.user, 'is_platform_admin', False):
            from clubs.models import Club
            ctx['pending_clubs_count'] = Club.objects.filter(status='pending').count()
    return ctx
