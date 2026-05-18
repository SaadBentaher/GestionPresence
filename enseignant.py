# ============================================================
#  enseignant.py  –  Fonctions réservées à l'Enseignant
# ============================================================

import data

# ---- Utilitaire --------------------------------------------

def _find_by_id(liste, uid):
    for item in liste:
        if uid in item:
            return item[uid]
    return None


# ============================================================
#  CONSULTATION DES SÉANCES (filtrée par enseignant)
# ============================================================

def consulter_mes_seances(eid):
    """Affiche les séances attribuées à l'enseignant connecté."""
    print(f"\n{'─'*60}")
    print("  MES SÉANCES")
    print(f"{'─'*60}")

    mes_seances = []
    for item in data.seances:
        for sid, s in item.items():
            if s["enseignant_id"] == eid:
                mes_seances.append((sid, s))

    if not mes_seances:
        print("  (aucune séance assignée)")
        print(f"{'─'*60}")
        return

    for sid, s in mes_seances:
        mod_info  = _find_by_id(data.modules, s["module_id"])
        mod_label = mod_info["intitule"] if mod_info else f"Module#{s['module_id']}"
        nb        = len(s["etudiants_ids"])
        nb_saisis = sum(1 for v in s["presences"].values() if v is not None)
        statut    = "✅ Complète" if nb_saisis == nb else f"⏳ {nb_saisis}/{nb} saisies"
        print(f"  [ID:{sid}]  {s['date']} {s['heure']}  |  {mod_label}")
        print(f"         Étudiants : {nb}  |  {statut}")
    print(f"{'─'*60}")


# ============================================================
#  SAISIE DES PRÉSENCES
# ============================================================

def saisir_presences(eid):
    """Permet à l'enseignant de marquer présent/absent chaque étudiant."""
    consulter_mes_seances(eid)

    try:
        sid = int(input("ID de la séance : "))
    except ValueError:
        print("❌ ID invalide."); return

    seance = _find_by_id(data.seances, sid)
    if not seance:
        print("❌ Séance introuvable."); return
    if seance["enseignant_id"] != eid:
        print("❌ Cette séance ne vous est pas attribuée."); return

    mod_info  = _find_by_id(data.modules, seance["module_id"])
    mod_label = mod_info["intitule"] if mod_info else "Module inconnu"
    print(f"\n  Saisie des présences — {seance['date']} {seance['heure']}  |  {mod_label}")
    print("  (Entrez 'p' = Présent, 'a' = Absent, 'Entrée' = ignorer)")
    print(f"  {'─'*45}")

    for etid in seance["etudiants_ids"]:
        et     = _find_by_id(data.etudiants, etid)
        nom    = et["nom"] if et else f"Étudiant#{etid}"
        actuel = seance["presences"].get(etid)

        if actuel is True:
            actuel_label = "Présent"
        elif actuel is False:
            actuel_label = "Absent"
        else:
            actuel_label = "Non saisi"

        rep = input(f"  {nom:<25} [{actuel_label}] p/a : ").strip().lower()

        if rep == "p":
            seance["presences"][etid] = True
        elif rep == "a":
            seance["presences"][etid] = False
        # Entrée vide → on conserve la valeur actuelle

    print("\n  ✅ Présences enregistrées.")
    _afficher_recap_presences(seance)


def _afficher_recap_presences(seance):
    """Affiche un récapitulatif après saisie."""
    presents = sum(1 for v in seance["presences"].values() if v is True)
    absents  = sum(1 for v in seance["presences"].values() if v is False)
    non_saisis = sum(1 for v in seance["presences"].values() if v is None)
    total = len(seance["presences"])
    print(f"\n  Récapitulatif : {presents} présent(s)  |  "
          f"{absents} absent(s)  |  {non_saisis} non saisi(s)  /  {total}")


# ============================================================
#  VOIR LE DÉTAIL COMPLET D'UNE SÉANCE
# ============================================================

def voir_detail_seance(eid):
    consulter_mes_seances(eid)
    try:
        sid = int(input("ID de la séance à détailler : "))
    except ValueError:
        print("❌ ID invalide."); return

    seance = _find_by_id(data.seances, sid)
    if not seance:
        print("❌ Séance introuvable."); return
    if seance["enseignant_id"] != eid:
        print("❌ Cette séance ne vous est pas attribuée."); return

    mod_info  = _find_by_id(data.modules, seance["module_id"])
    mod_label = mod_info["intitule"] if mod_info else "?"
    print(f"\n  Séance [{sid}]  —  {seance['date']} {seance['heure']}")
    print(f"  Module : {mod_label}")
    print(f"  {'─'*45}")
    print(f"  {'Nom':<25} {'CNE':<12} {'Présence'}")
    print(f"  {'─'*45}")
    for etid, statut in seance["presences"].items():
        et  = _find_by_id(data.etudiants, etid)
        nom = et["nom"] if et else f"Étudiant#{etid}"
        cne = et["cne"] if et else "-"
        s   = "✅ Présent" if statut is True else ("❌ Absent" if statut is False else "⏳ Non saisi")
        print(f"  {nom:<25} {cne:<12} {s}")


# ============================================================
#  MENU ENSEIGNANT
# ============================================================

def menu_enseignant(eid):
    info = _find_by_id(data.enseignants, eid)
    nom  = info["nom"] if info else "Enseignant"

    while True:
        print(f"\n{'═'*45}")
        print(f"  MENU ENSEIGNANT  ({nom})")
        print(f"{'═'*45}")
        print("  1. Consulter mes séances")
        print("  2. Saisir les présences")
        print("  3. Voir le détail d'une séance")
        print("  0. Déconnexion")
        print(f"{'═'*45}")

        choix = input("  Votre choix : ").strip()

        if choix == "1":
            consulter_mes_seances(eid)
        elif choix == "2":
            saisir_presences(eid)
        elif choix == "3":
            voir_detail_seance(eid)
        elif choix == "0":
            print("  👋 Déconnexion. À bientôt !")
            break
        else:
            print("  ❌ Option invalide.")
