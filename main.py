#!/usr/bin/env python3
# ============================================================
#  main.py  –  Programme principal
#  Projet : Gestion des présences aux séances de cours
#  EMSI — 3ème année IIR  —  Python & Framework 2025/2026
# ============================================================

import authentification
import admin
import enseignant


def afficher_banniere():
    print("""
╔══════════════════════════════════════════════════════╗
║     GESTION DES PRÉSENCES — SÉANCES DE COURS         ║
║     EMSI  |  Ingénierie Informatique et Réseaux      ║
╚══════════════════════════════════════════════════════╝
""")


def menu_principal():
    """Menu d'accueil avant authentification."""
    while True:
        print("\n===== ACCUEIL =====")
        print("1. Se connecter")
        print("2. Créer un compte")
        print("0. Quitter")

        choix = input("Votre choix : ").strip()

        if choix == "1":
            resultat = authentification.connexion()
            if resultat:
                role, uid, _ = resultat
                if role == "admin":
                    admin.menu_admin(uid)
                elif role == "enseignant":
                    enseignant.menu_enseignant(uid)

        elif choix == "2":
            authentification.inscription()

        elif choix == "0":
            print("\n  Au revoir ! 👋\n")
            break

        else:
            print("❌ Choix invalide.")


# ============================================================
#  Point d'entrée
# ============================================================

if __name__ == "__main__":
    afficher_banniere()
    menu_principal()
