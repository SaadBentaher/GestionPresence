from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone


class ClubCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fa-users')
    color = models.CharField(max_length=7, default='#6366F1')
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def get_club_count(self):
        return self.clubs.filter(status='approved').count()


class Club(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_SUSPENDED = 'suspended'

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
        ('suspended', 'Suspendu'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    category = models.ForeignKey(
        ClubCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='clubs'
    )
    logo = models.ImageField(upload_to='clubs/logos/', null=True, blank=True)
    banner = models.ImageField(upload_to='clubs/banners/', null=True, blank=True)
    founding_date = models.DateField(null=True, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='created_clubs'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    max_members = models.PositiveIntegerField(default=0, help_text='0 = illimité')
    tags = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Club'
        verbose_name_plural = 'Clubs'
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            n = 1
            while Club.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def member_count(self):
        return self.memberships.filter(status='approved').count()

    @property
    def is_approved(self):
        return self.status == self.STATUS_APPROVED

    def get_approved_members(self):
        return self.memberships.filter(status='approved').select_related('user')

    def get_managers(self):
        return self.memberships.filter(
            status='approved', role__in=['owner', 'manager']
        ).select_related('user')

    def get_tag_list(self):
        if self.tags:
            return [t.strip() for t in self.tags.split(',') if t.strip()]
        return []

    def user_membership(self, user):
        if not user.is_authenticated:
            return None
        return self.memberships.filter(user=user).first()


class Membership(models.Model):
    ROLE_OWNER = 'owner'
    ROLE_MANAGER = 'manager'
    ROLE_MEMBER = 'member'

    ROLE_CHOICES = [
        ('owner', 'Fondateur'),
        ('manager', 'Responsable'),
        ('member', 'Membre'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_LEFT = 'left'

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
        ('left', 'Quitté'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='memberships'
    )
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    joined_at = models.DateTimeField(null=True, blank=True)
    left_at = models.DateTimeField(null=True, blank=True)
    join_message = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='invitations_sent'
    )

    class Meta:
        verbose_name = 'Adhésion'
        verbose_name_plural = 'Adhésions'
        unique_together = ('user', 'club')
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.user} — {self.club} ({self.get_status_display()})"

    def approve(self):
        self.status = self.STATUS_APPROVED
        self.joined_at = timezone.now()
        self.save(update_fields=['status', 'joined_at'])

    def reject(self, reason=''):
        self.status = self.STATUS_REJECTED
        self.rejection_reason = reason
        self.save(update_fields=['status', 'rejection_reason'])

    def leave(self):
        self.status = self.STATUS_LEFT
        self.left_at = timezone.now()
        self.save(update_fields=['status', 'left_at'])

    @property
    def is_active(self):
        return self.status == self.STATUS_APPROVED

    @property
    def is_pending(self):
        return self.status == self.STATUS_PENDING

    @property
    def can_manage(self):
        return self.status == self.STATUS_APPROVED and self.role in (self.ROLE_OWNER, self.ROLE_MANAGER)


class Announcement(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=300)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Annonce'
        verbose_name_plural = 'Annonces'
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"{self.club.name} — {self.title}"
