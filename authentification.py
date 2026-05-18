# ============================================================
#  authentification.py  –  Inscription & Connexion
# ============================================================

import data

# ---- Helpers -----------------------------------------------

def _get_all_data(liste):
    """Retourne le dictionnaire interne d'un élément de liste."""
    for item in liste:
        for k, v in item.items():
            return k, v          # (id, données)
    return None, None


def _next_id(liste):
    """Génère le prochain identifiant disponible."""
    if not liste:
        return 1
    ids = [list(item.keys())[0] for item in liste]
    return max(ids) + 1


def _email_existe(email):
    """Vérifie qu'un email n'est pas déjà utilisé."""
    for pool in [data.administrateurs, data.enseignants]:
        for item in pool:
            for uid, info in item.items():
                if info["email"] == email:
                    return True
    return False


# ---- Inscription -------------------------------------------

def inscription():
    """Crée un nouveau compte (admin ou enseignant)."""
    print("\n===== INSCRIPTION =====")
    print("1. Administrateur")
    print("2. Enseignant")
    choix = input("Type de compte : ").strip()

    if choix not in ("1", "2"):
        print("❌ Choix invalide.")
        return None

    nom    = input("Nom complet    : ").strip()
    email  = input("Email          : ").strip()
    mdp    = input("Mot de passe   : ").strip()

    if not nom or not email or not mdp:
        print("❌ Tous les champs sont obligatoires.")
        return None

    if _email_existe(email):
        print("❌ Cet email est déjà utilisé.")
        return None

    if choix == "1":
        uid = _next_id(data.administrateurs)
        data.administrateurs.append({uid: {"nom": nom, "email": email, "password": mdp}})
        print(f"✅ Administrateur '{nom}' créé avec l'ID {uid}.")
        return ("admin", uid)
    else:
        uid = _next_id(data.enseignants)
        data.enseignants.append({uid: {"nom": nom, "email": email, "password": mdp}})
        print(f"✅ Enseignant '{nom}' créé avec l'ID {uid}.")
        return ("enseignant", uid)


# ---- Connexion ---------------------------------------------

def connexion():
    """
    Authentifie un utilisateur.
    Retourne (role, uid, info) ou None après 3 échecs.
    """
    print("\n===== CONNEXION =====")
    tentatives = 0

    while tentatives < 3:
        email = input("Email        : ").strip()
        mdp   = input("Mot de passe : ").strip()

        # Recherche dans administrateurs
        for item in data.administrateurs:
            for uid, info in item.items():
                if info["email"] == email and info["password"] == mdp:
                    print(f"\n✅ Bienvenue, {info['nom']} (Administrateur) !")
                    return ("admin", uid, info)

        # Recherche dans enseignants
        for item in data.enseignants:
            for uid, info in item.items():
                if info["email"] == email and info["password"] == mdp:
                    print(f"\n✅ Bienvenue, {info['nom']} (Enseignant) !")
                    return ("enseignant", uid, info)

        tentatives += 1
        restantes = 3 - tentatives
        if restantes > 0:
            print(f"❌ Email ou mot de passe incorrect. ({restantes} tentative(s) restante(s))")
        else:
            print("❌ Trop de tentatives. Accès bloqué.")

    return None
