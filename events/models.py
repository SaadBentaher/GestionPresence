from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone


class Event(models.Model):
    TYPE_IN_PERSON = 'in_person'
    TYPE_ONLINE = 'online'
    TYPE_HYBRID = 'hybrid'

    TYPE_CHOICES = [
        ('in_person', 'En présentiel'),
        ('online', 'En ligne'),
        ('hybrid', 'Hybride'),
    ]

    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_CANCELLED = 'cancelled'
    STATUS_PAST = 'past'

    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
        ('cancelled', 'Annulé'),
    ]

    club = models.ForeignKey(
        'clubs.Club', on_delete=models.CASCADE, related_name='events'
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='in_person')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=500, blank=True)
    location_url = models.URLField(blank=True)
    cover_image = models.ImageField(upload_to='events/covers/', null=True, blank=True)
    capacity = models.PositiveIntegerField(default=0, help_text='0 = illimité')
    registration_deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='created_events'
    )
    tags = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Événement'
        verbose_name_plural = 'Événements'
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.title} — {self.date}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            n = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def is_past(self):
        return self.date < timezone.now().date()

    @property
    def is_today(self):
        return self.date == timezone.now().date()

    @property
    def registration_count(self):
        return self.registrations.filter(status='registered').count()

    @property
    def spots_remaining(self):
        if self.capacity == 0:
            return None
        taken = self.registrations.filter(status='registered').count()
        return max(0, self.capacity - taken)

    @property
    def is_registration_open(self):
        if self.status != 'published':
            return False
        if self.is_past:
            return False
        if self.registration_deadline and timezone.now() > self.registration_deadline:
            return False
        if self.capacity > 0 and self.spots_remaining == 0:
            return False
        return True

    def get_tag_list(self):
        if self.tags:
            return [t.strip() for t in self.tags.split(',') if t.strip()]
        return []


class EventRegistration(models.Model):
    STATUS_REGISTERED = 'registered'
    STATUS_ATTENDED = 'attended'
    STATUS_CANCELLED = 'cancelled'
    STATUS_WAITLISTED = 'waitlisted'

    STATUS_CHOICES = [
        ('registered', 'Inscrit'),
        ('attended', 'Présent'),
        ('cancelled', 'Annulé'),
        ('waitlisted', 'Liste d\'attente'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='event_registrations'
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Inscription'
        verbose_name_plural = 'Inscriptions'
        unique_together = ('event', 'user')
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user} → {self.event.title}"
