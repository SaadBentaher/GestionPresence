# ============================================================
#  data.py  –  Stockage des données (listes + dictionnaires)
#  Projet : Gestion des présences aux séances de cours
# ============================================================

# ---------- Utilisateurs ----------
administrateurs = [
    {1: {"nom": "Admin Principal", "email": "admin@emsi.ma", "password": "admin123"}}
]

enseignants = [
    {1: {"nom": "Sara Alami",   "email": "sara@emsi.ma",   "password": "sara123"}},
    {2: {"nom": "Karim Fassi",  "email": "karim@emsi.ma",  "password": "karim123"}},
]

# ---------- Étudiants ----------
etudiants = [
    {1: {"nom": "Ali Benali",      "cne": "G110001", "filiere": "IIR3"}},
    {2: {"nom": "Fatima Zohra",    "cne": "G110002", "filiere": "IIR3"}},
    {3: {"nom": "Youssef El Idri", "cne": "G110003", "filiere": "IIR3"}},
]

# ---------- Modules ----------
modules = [
    {1: {"code": "PY301",  "intitule": "Programmation Python & Framework", "filiere": "IIR3"}},
    {2: {"code": "BD302",  "intitule": "Bases de Données Avancées",        "filiere": "IIR3"}},
]

# ---------- Séances ----------
# Structure : { id: { module_id, date, heure, enseignant_id,
#                     etudiants_ids: [...],
#                     presences: { etudiant_id: True/False/None } } }
seances = []
