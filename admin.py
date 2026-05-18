# ============================================================
#  admin.py  –  Fonctions réservées à l'Administrateur
# ============================================================

import data

# ============================================================
#  UTILITAIRES
# ============================================================

def _next_id(liste):
    if not liste:
        return 1
    return max(list(item.keys())[0] for item in liste) + 1


def _find_by_id(liste, uid):
    """Retourne le dict interne d'un élément ou None."""
    for item in liste:
        if uid in item:
            return item[uid]
    return None


def _afficher_tableau(liste, champs, titre):
    """Affiche une liste sous forme de tableau simple."""
    print(f"\n{'─'*50}")
    print(f"  {titre}")
    print(f"{'─'*50}")
    if not liste:
        print("  (aucun enregistrement)")
    for item in liste:
        for uid, info in item.items():
            ligne = f"  [ID:{uid}]"
            for c in champs:
                ligne += f"  {c}: {info.get(c, '-')}"
            print(ligne)
    print(f"{'─'*50}")


# ============================================================
#  GESTION DES ÉTUDIANTS
# ============================================================

def ajouter_etudiant():
    print("\n-- Ajouter un étudiant --")
    nom     = input("Nom complet : ").strip()
    cne     = input("CNE         : ").strip()
    filiere = input("Filière     : ").strip()
    if not nom or not cne:
        print("❌ Nom et CNE obligatoires."); return
    # Vérifier unicité CNE
    for item in data.etudiants:
        for uid, info in item.items():
            if info["cne"] == cne:
                print("❌ Ce CNE existe déjà."); return
    uid = _next_id(data.etudiants)
    data.etudiants.append({uid: {"nom": nom, "cne": cne, "filiere": filiere}})
    print(f"✅ Étudiant ajouté avec l'ID {uid}.")


def modifier_etudiant():
    print("\n-- Modifier un étudiant --")
    consulter_etudiants()
    try:
        uid = int(input("ID à modifier : "))
    except ValueError:
        print("❌ ID invalide."); return
    info = _find_by_id(data.etudiants, uid)
    if not info:
        print("❌ Étudiant introuvable."); return
    nom     = input(f"Nouveau nom [{info['nom']}]         : ").strip() or info["nom"]
    filiere = input(f"Nouvelle filière [{info['filiere']}] : ").strip() or info["filiere"]
    info["nom"]     = nom
    info["filiere"] = filiere
    print("✅ Étudiant modifié.")


def supprimer_etudiant():
    print("\n-- Supprimer un étudiant --")
    consulter_etudiants()
    try:
        uid = int(input("ID à supprimer : "))
    except ValueError:
        print("❌ ID invalide."); return
    for i, item in enumerate(data.etudiants):
        if uid in item:
            conf = input(f"Confirmer la suppression de '{item[uid]['nom']}' ? (o/n) : ")
            if conf.lower() == "o":
                data.etudiants.pop(i)
                print("✅ Étudiant supprimé.")
            return
    print("❌ Étudiant introuvable.")


def consulter_etudiants():
    _afficher_tableau(data.etudiants, ["nom", "cne", "filiere"], "LISTE DES ÉTUDIANTS")


def rechercher_etudiant():
    terme = input("Rechercher (nom ou CNE) : ").strip().lower()
    resultats = []
    for item in data.etudiants:
        for uid, info in item.items():
            if terme in info["nom"].lower() or terme in info["cne"].lower():
                resultats.append({uid: info})
    if resultats:
        _afficher_tableau(resultats, ["nom", "cne", "filiere"], f"Résultats pour '{terme}'")
    else:
        print("❌ Aucun résultat trouvé.")


# ============================================================
#  GESTION DES MODULES
# ============================================================

def ajouter_module():
    print("\n-- Ajouter un module --")
    code     = input("Code        : ").strip()
    intitule = input("Intitulé    : ").strip()
    filiere  = input("Filière     : ").strip()
    if not code or not intitule:
        print("❌ Code et intitulé obligatoires."); return
    uid = _next_id(data.modules)
    data.modules.append({uid: {"code": code, "intitule": intitule, "filiere": filiere}})
    print(f"✅ Module ajouté avec l'ID {uid}.")


def modifier_module():
    print("\n-- Modifier un module --")
    consulter_modules()
    try:
        uid = int(input("ID à modifier : "))
    except ValueError:
        print("❌ ID invalide."); return
    info = _find_by_id(data.modules, uid)
    if not info:
        print("❌ Module introuvable."); return
    info["intitule"] = input(f"Intitulé [{info['intitule']}] : ").strip() or info["intitule"]
    info["filiere"]  = input(f"Filière [{info['filiere']}]   : ").strip() or info["filiere"]
    print("✅ Module modifié.")


def supprimer_module():
    print("\n-- Supprimer un module --")
    consulter_modules()
    try:
        uid = int(input("ID à supprimer : "))
    except ValueError:
        print("❌ ID invalide."); return
    for i, item in enumerate(data.modules):
        if uid in item:
            conf = input(f"Confirmer ? (o/n) : ")
            if conf.lower() == "o":
                data.modules.pop(i)
                print("✅ Module supprimé.")
            return
    print("❌ Module introuvable.")


def consulter_modules():
    _afficher_tableau(data.modules, ["code", "intitule", "filiere"], "LISTE DES MODULES")


# ============================================================
#  GESTION DES ENSEIGNANTS
# ============================================================

def ajouter_enseignant():
    print("\n-- Ajouter un enseignant --")
    nom   = input("Nom complet  : ").strip()
    email = input("Email        : ").strip()
    mdp   = input("Mot de passe : ").strip()
    if not nom or not email or not mdp:
        print("❌ Tous les champs sont obligatoires."); return
    uid = _next_id(data.enseignants)
    data.enseignants.append({uid: {"nom": nom, "email": email, "password": mdp}})
    print(f"✅ Enseignant ajouté avec l'ID {uid}.")


def consulter_enseignants():
    _afficher_tableau(data.enseignants, ["nom", "email"], "LISTE DES ENSEIGNANTS")


# ============================================================
#  GESTION DES SÉANCES
# ============================================================

def creer_seance():
    print("\n-- Créer une séance --")

    # Choisir le module
    consulter_modules()
    try:
        mid = int(input("ID du module : "))
    except ValueError:
        print("❌ ID invalide."); return
    if not _find_by_id(data.modules, mid):
        print("❌ Module introuvable."); return

    # Date et heure
    date  = input("Date (JJ/MM/AAAA) : ").strip()
    heure = input("Heure (HH:MM)     : ").strip()

    # Choisir l'enseignant
    consulter_enseignants()
    try:
        eid = int(input("ID de l'enseignant : "))
    except ValueError:
        print("❌ ID invalide."); return
    if not _find_by_id(data.enseignants, eid):
        print("❌ Enseignant introuvable."); return

    # Sélectionner les étudiants
    consulter_etudiants()
    saisie = input("IDs des étudiants (séparés par virgule) : ").strip()
    try:
        eids = [int(x.strip()) for x in saisie.split(",") if x.strip()]
    except ValueError:
        print("❌ Format IDs invalide."); return

    eids_valides = [e for e in eids if _find_by_id(data.etudiants, e)]
    if not eids_valides:
        print("❌ Aucun étudiant valide sélectionné."); return

    # Créer la séance avec présences initialisées à None
    sid = _next_id(data.seances) if data.seances else 1
    presences = {e: None for e in eids_valides}   # None = non encore saisi

    data.seances.append({sid: {
        "module_id":    mid,
        "date":         date,
        "heure":        heure,
        "enseignant_id": eid,
        "etudiants_ids": eids_valides,
        "presences":    presences
    }})
    print(f"✅ Séance créée avec l'ID {sid} ({len(eids_valides)} étudiant(s)).")


def consulter_seances():
    """Affiche toutes les séances avec détails."""
    print(f"\n{'─'*60}")
    print("  LISTE DES SÉANCES")
    print(f"{'─'*60}")
    if not data.seances:
        print("  (aucune séance)"); print(f"{'─'*60}"); return

    for item in data.seances:
        for sid, s in item.items():
            mod_info = _find_by_id(data.modules, s["module_id"])
            ens_info = _find_by_id(data.enseignants, s["enseignant_id"])
            mod_label = mod_info["intitule"] if mod_info else f"Module#{s['module_id']}"
            ens_label = ens_info["nom"]      if ens_info else f"Enseignant#{s['enseignant_id']}"
            nb_etudiants = len(s["etudiants_ids"])
            nb_saisis    = sum(1 for v in s["presences"].values() if v is not None)
            print(f"  [ID:{sid}]  {s['date']} {s['heure']}  |  {mod_label}")
            print(f"         Enseignant : {ens_label}")
            print(f"         Étudiants  : {nb_etudiants}  |  Présences saisies : {nb_saisis}/{nb_etudiants}")
    print(f"{'─'*60}")


def voir_presences_seance():
    """Affiche le détail des présences pour une séance."""
    consulter_seances()
    try:
        sid = int(input("ID de la séance : "))
    except ValueError:
        print("❌ ID invalide."); return
    seance = _find_by_id(data.seances, sid)
    if not seance:
        print("❌ Séance introuvable."); return

    print(f"\n  Présences — Séance {sid} ({seance['date']} {seance['heure']})")
    print(f"  {'Étudiant':<25} {'CNE':<12} {'Présence'}")
    print(f"  {'─'*50}")
    for eid, statut in seance["presences"].items():
        et = _find_by_id(data.etudiants, eid)
        nom = et["nom"] if et else f"Étudiant#{eid}"
        cne = et["cne"] if et else "-"
        if statut is True:
            s = "✅ Présent"
        elif statut is False:
            s = "❌ Absent"
        else:
            s = "⏳ Non saisi"
        print(f"  {nom:<25} {cne:<12} {s}")


# ============================================================
#  MENU ADMINISTRATEUR
# ============================================================

def menu_admin(uid_admin):
    info = _find_by_id(data.administrateurs, uid_admin)
    nom  = info["nom"] if info else "Administrateur"

    while True:
        print(f"\n{'═'*45}")
        print(f"  MENU ADMINISTRATEUR  ({nom})")
        print(f"{'═'*45}")
        print("  ── Étudiants ──")
        print("  1. Ajouter un étudiant")
        print("  2. Modifier un étudiant")
        print("  3. Supprimer un étudiant")
        print("  4. Consulter les étudiants")
        print("  5. Rechercher un étudiant")
        print("  ── Modules ──")
        print("  6. Ajouter un module")
        print("  7. Modifier un module")
        print("  8. Supprimer un module")
        print("  9. Consulter les modules")
        print("  ── Enseignants ──")
        print(" 10. Ajouter un enseignant")
        print(" 11. Consulter les enseignants")
        print("  ── Séances ──")
        print(" 12. Créer une séance")
        print(" 13. Consulter les séances")
        print(" 14. Voir les présences d'une séance")
        print("  ───────────────")
        print("  0. Déconnexion")
        print(f"{'═'*45}")

        choix = input("  Votre choix : ").strip()

        actions = {
            "1":  ajouter_etudiant,
            "2":  modifier_etudiant,
            "3":  supprimer_etudiant,
            "4":  consulter_etudiants,
            "5":  rechercher_etudiant,
            "6":  ajouter_module,
            "7":  modifier_module,
            "8":  supprimer_module,
            "9":  consulter_modules,
            "10": ajouter_enseignant,
            "11": consulter_enseignants,
            "12": creer_seance,
            "13": consulter_seances,
            "14": voir_presences_seance,
        }

        if choix == "0":
            print("  👋 Déconnexion. À bientôt !")
            break
        elif choix in actions:
            actions[choix]()
        else:
            print("  ❌ Option invalide.")
