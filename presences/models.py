from django.db import models
from django.contrib.auth.models import AbstractUser


class Utilisateur(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_ENSEIGNANT = 'enseignant'
    ROLE_ETUDIANT = 'etudiant'
    ROLE_CLUB_MANAGER = 'club_manager'

    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('enseignant', 'Enseignant'),
        ('etudiant', 'Étudiant'),
        ('club_manager', 'Responsable de Club'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='etudiant')

    # Attendance-specific
    cne = models.CharField(max_length=20, blank=True, null=True)
    filiere = models.CharField(max_length=50, blank=True, null=True)

    # Profile
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    university = models.CharField(max_length=200, blank=True, default='EMSI')
    website = models.URLField(blank=True, default='')
    linkedin = models.URLField(blank=True, default='')

    @property
    def is_student(self):
        return self.role == self.ROLE_ETUDIANT

    @property
    def is_club_manager(self):
        return self.role in (self.ROLE_CLUB_MANAGER, self.ROLE_ADMIN)

    @property
    def is_platform_admin(self):
        return self.role == self.ROLE_ADMIN

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None

    def get_initials(self):
        parts = []
        if self.first_name:
            parts.append(self.first_name[0].upper())
        if self.last_name:
            parts.append(self.last_name[0].upper())
        if not parts:
            parts.append(self.username[0].upper())
        return ''.join(parts[:2])

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Module(models.Model):
    code = models.CharField(max_length=10, unique=True)
    intitule = models.CharField(max_length=100)
    filiere = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code} - {self.intitule}"


class Seance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(
        Utilisateur, on_delete=models.CASCADE,
        limit_choices_to={'role': 'enseignant'}
    )
    date = models.DateField()
    heure = models.TimeField()

    def __str__(self):
        return f"{self.module.code} - {self.date} {self.heure}"


class Presence(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name='presences')
    etudiant = models.ForeignKey(
        Utilisateur, on_delete=models.CASCADE,
        limit_choices_to={'role': 'etudiant'}
    )
    est_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('seance', 'etudiant')

    def __str__(self):
        statut = 'Présent' if self.est_present else 'Absent'
        return f"{self.etudiant} - {self.seance} : {statut}"
