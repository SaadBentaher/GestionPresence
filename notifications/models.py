from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_JOIN_REQUEST = 'join_request'
    TYPE_JOIN_APPROVED = 'join_approved'
    TYPE_JOIN_REJECTED = 'join_rejected'
    TYPE_NEW_EVENT = 'new_event'
    TYPE_NEW_ANNOUNCEMENT = 'new_announcement'
    TYPE_CLUB_APPROVED = 'club_approved'
    TYPE_CLUB_REJECTED = 'club_rejected'
    TYPE_MEMBER_JOINED = 'member_joined'
    TYPE_EVENT_REMINDER = 'event_reminder'

    TYPE_CHOICES = [
        ('join_request', 'Demande d\'adhésion'),
        ('join_approved', 'Adhésion approuvée'),
        ('join_rejected', 'Adhésion refusée'),
        ('new_event', 'Nouvel événement'),
        ('new_announcement', 'Nouvelle annonce'),
        ('club_approved', 'Club approuvé'),
        ('club_rejected', 'Club rejeté'),
        ('member_joined', 'Nouveau membre'),
        ('event_reminder', 'Rappel événement'),
    ]

    TYPE_ICONS = {
        'join_request': 'fa-user-plus',
        'join_approved': 'fa-circle-check',
        'join_rejected': 'fa-circle-xmark',
        'new_event': 'fa-calendar-plus',
        'new_announcement': 'fa-bullhorn',
        'club_approved': 'fa-shield-check',
        'club_rejected': 'fa-shield-xmark',
        'member_joined': 'fa-user-group',
        'event_reminder': 'fa-bell',
    }

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='notifications'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='sent_notifications'
    )
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    title = models.CharField(max_length=300)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient} — {self.title}"

    def mark_read(self):
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

    def get_icon(self):
        return self.TYPE_ICONS.get(self.notification_type, 'fa-bell')


def notify(recipient, notification_type, title, message, link='', sender=None):
    Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        title=title,
        message=message,
        link=link,
    )
