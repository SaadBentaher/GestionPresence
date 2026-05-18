from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('enseignant', 'Enseignant'),
        ('etudiant', 'Étudiant'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='etudiant')
    
    # Pour les étudiants
    cne = models.CharField(max_length=20, blank=True, null=True)
    filiere = models.CharField(max_length=50, blank=True, null=True)

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
    enseignant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, limit_choices_to={'role': 'enseignant'})
    date = models.DateField()
    heure = models.TimeField()

    def __str__(self):
        return f"{self.module.code} - {self.date} {self.heure}"

class Presence(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, related_name='presences')
    etudiant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, limit_choices_to={'role': 'etudiant'})
    est_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('seance', 'etudiant')

    def __str__(self):
        return f"{self.etudiant} - {self.seance} : {'Présent' if self.est_present else 'Absent'}"
