# Gestion des Présences EMSI

Bienvenue dans le projet de **Gestion des Présences EMSI**, une application web moderne développée en **Python** et **Django**. Initialement conçue comme un script en ligne de commande, cette plateforme a été entièrement repensée pour offrir une interface utilisateur dynamique, ergonomique et visuellement attrayante (basée sur le style "Glassmorphism").

## 🌟 Fonctionnalités Principales

L'application est divisée en plusieurs espaces dédiés, adaptés au rôle de chaque utilisateur :

*   **Espace Administrateur :**
    *   Tableau de bord global avec des statistiques en temps réel (nombre total d'étudiants, enseignants, modules et séances).
    *   Accès direct au panneau d'administration natif de Django pour une gestion complète de la base de données.
*   **Espace Enseignant :**
    *   Création et planification de nouvelles séances de cours.
    *   Consultation de la liste de ses séances.
    *   Système de pointage intuitif (cases à cocher) pour marquer la présence ou l'absence des étudiants pour chaque séance.
*   **Espace Étudiant :**
    *   Tableau de bord personnel affichant l'historique complet des présences et absences.
    *   Calcul et affichage automatique du taux de présence global (en pourcentage).
*   **Design & Interface :**
    *   Utilisation de CSS moderne (Vanilla CSS) avec des effets de flou (backdrop-filter) et des dégradés.
    *   Entièrement responsive et adapté à toutes les tailles d'écrans.

---

## 🛠️ Prérequis

Assurez-vous d'avoir installé **Python 3.8+** sur votre machine.

---

## 🚀 Installation et Exécution

Voici les étapes à suivre pour lancer l'application sur votre machine locale.

### 1. Ouvrir le terminal dans le dossier du projet
Ouvrez votre terminal (PowerShell, CMD, ou le terminal intégré de votre IDE) et assurez-vous d'être à la racine du projet `MiniProjet`.

### 2. Activer l'environnement virtuel
L'application dépend de plusieurs paquets (comme Django). Pour isoler ces dépendances, un environnement virtuel (`venv`) est inclus ou doit être créé. Activez-le avec la commande suivante :

**Sur Windows (PowerShell) :**
```powershell
.\venv\Scripts\activate
```

*(Vous devriez voir `(venv)` apparaître au début de votre ligne de commande)*.

> **Note :** Si les dépendances ne sont pas installées, vous pouvez les installer via : `pip install django`

### 3. Lancer le serveur de développement
Une fois l'environnement virtuel activé, démarrez le serveur web Django avec la commande suivante :

```powershell
python manage.py runserver
```

### 4. Accéder à l'application
Ouvrez votre navigateur web préféré (Chrome, Firefox, Edge, etc.) et rendez-vous à l'adresse suivante :

**👉 http://127.0.0.1:8000/**

---

## 🔑 Comptes de Test (Démo)

La base de données a été pré-remplie avec des données d'exemple pour faciliter les tests de l'application. Vous pouvez utiliser les identifiants suivants :

| Rôle | Nom d'utilisateur | Mot de passe |
| :--- | :--- | :--- |
| **Administrateur** | `admin` | `admin123` |
| **Enseignant** | `sara` | `sara123` |
| **Enseignant** | `karim` | `karim123` |
| **Étudiant** | `etud1` | `etud123` |
| **Étudiant** | `etud2` | `etud123` |
| **Étudiant** | `etud3` | `etud123` |

---

*Développé dans le cadre du projet Python & Framework 2025/2026 - EMSI (IIR 3ème année).*
