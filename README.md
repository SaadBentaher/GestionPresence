# ClubHub — Plateforme Web de Gestion de Clubs Étudiants

Une application web moderne de gestion de clubs étudiants développée avec **Django 6**, offrant un système complet de gestion de clubs, d'événements, de membres et de notifications avec un design professionnel supportant les thèmes clair et sombre.

---

## Aperçu

ClubHub permet aux étudiants de découvrir et rejoindre des clubs, aux responsables de gérer leurs clubs et événements, et aux administrateurs de superviser l'ensemble de la plateforme. L'interface s'inspire des designs de produits SaaS modernes (Notion, Linear, GitHub) avec une sidebar fixe, un système de navigation par rôle et un toggle thème clair/sombre.

---

## Fonctionnalités

### Gestion des clubs
- Création de clubs avec logo, bannière, description, catégorie et liens sociaux
- Workflow d'approbation : les clubs soumis attendent validation par un administrateur
- Système d'adhésion avec rôles : Propriétaire, Gestionnaire, Membre
- Annonces épinglables visibles par les membres
- Page de gestion dédiée pour les responsables (demandes en attente, membres, annonces)

### Gestion des événements
- Création d'événements liés à un club (présentiel, en ligne, hybride)
- Inscription des étudiants avec gestion des places et délai d'inscription
- Statuts : Brouillon, Publié, Annulé

### Système de notifications
- Notifications automatiques pour les demandes d'adhésion, approbations, rejets, nouveaux événements et annonces
- Badge non-lu dans la sidebar, marquage tout lu, compteur JSON pour le dot topbar

### Rôles utilisateurs
| Rôle | Capacités |
|---|---|
| **Administrateur** | Valider/rejeter/suspendre les clubs, gérer les utilisateurs, accès admin Django |
| **Responsable de club** | Créer et gérer un club, approuver des membres, créer des événements et annonces |
| **Étudiant** | Découvrir des clubs, demander à rejoindre, s'inscrire aux événements |

### Interface
- Design system complet avec variables CSS (Inter, palette Indigo)
- Thème clair / sombre avec persistance localStorage et transition fluide
- Sidebar fixe responsive (mobile : drawer avec overlay)
- Page d'accueil publique (landing page) avec catégories et clubs mis en avant

---

## Stack technique

| Couche | Technologie |
|---|---|
| Backend | Python 3.13, Django 6.0 |
| Base de données | SQLite |
| Auth | Session-based (django.contrib.auth) |
| Frontend | CSS custom (design system), Vanilla JS, Font Awesome 6 |
| Formulaires | django-widget-tweaks 1.5 |
| Images | Pillow 12.2 |

---

## Installation

### Prérequis
- Python 3.10+
- pip

### Étapes

**1. Cloner / ouvrir le projet**
```powershell
cd MiniProjet
```

**2. Créer et activer l'environnement virtuel**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**3. Installer les dépendances**
```powershell
pip install -r requirements.txt
```

**4. Appliquer les migrations**
```powershell
python manage.py migrate
```

**5. Peupler la base de données avec les données de démo**
```powershell
python manage.py seed
```

**6. Lancer le serveur de développement**
```powershell
python manage.py runserver
```

**7. Ouvrir le navigateur**

```
http://127.0.0.1:8000/
```

---

## Comptes de démonstration

| Rôle | Email | Mot de passe |
|---|---|---|
| Administrateur | `admin@emsi.ma` | `Admin123!` |
| Responsable de club | `sara.alami@emsi.ma` | `Sara123!` |
| Responsable de club | `karim.fassi@emsi.ma` | `Karim123!` |
| Étudiant | `ali.benali@emsi.ma` | `Student123!` |
| Étudiant | `fatima.z@emsi.ma` | `Student123!` |

---

## Structure du projet

```
MiniProjet/
├── core/                   # Configuration Django (settings, urls)
├── presences/              # App originale : gestion des présences en cours
│   └── models.py           # Modèle Utilisateur personnalisé (AbstractUser)
├── clubs/                  # Gestion des clubs, membres, annonces
│   ├── models.py           # Club, ClubCategory, Membership, Announcement
│   ├── views.py            # CRUD clubs, workflow adhésion, admin review
│   └── management/
│       └── commands/
│           └── seed.py     # Commande de peuplement de la BDD
├── events/                 # Gestion des événements et inscriptions
│   └── models.py           # Event, EventRegistration
├── notifications/          # Système de notifications
│   ├── models.py           # Notification + helper notify()
│   └── context_processors.py  # unread_notif_count, pending_clubs_count
├── templates/              # Templates Django (base.html + par app)
├── static/
│   ├── css/
│   │   ├── style.css       # Design system de base
│   │   ├── clubs.css       # Composants ClubHub + thème sombre
│   │   └── landing.css     # Page d'accueil publique
│   └── js/
│       └── main.js         # Toggle thème, sidebar mobile, alerts, etc.
└── media/                  # Fichiers uploadés (logos, bannières, avatars)
```

---

## Données de démonstration

Le script `seed` crée :
- **8 catégories** : Technologie & IA, Sports, Arts & Culture, Sciences, Entrepreneuriat, Littérature, Musique, Environnement
- **8 clubs** avec statuts variés (approuvés, en attente)
- **21 utilisateurs** (1 admin, 3 responsables, 17 étudiants)
- **57 adhésions** (approuvées et en attente)
- **6 événements** publiés avec inscriptions
- **Annonces** pour chaque club

---

## Thème clair / sombre

Le toggle est accessible dans le bas de la sidebar (icône lune/soleil). La préférence est sauvegardée dans `localStorage` et appliquée avant le premier rendu (via un script inline dans `<head>`) pour éviter tout flash de mauvais thème au chargement.

---

*Développé dans le cadre du projet Python & Framework 2025/2026 — EMSI, IIR 3ème année.*
