# Réglages par défaut d'une partie de DAO (spec V1, tableau « Départ »).
# Tous les autres fichiers lisent leurs valeurs ici.
# En US3, ces valeurs passeront dans un fichier de configuration.


# =====================================================================
# MEMBRES
# =====================================================================

# Nombre de membres de chaque profil, dans l'ordre où ils sont créés.
# « Membre 1 » à « Membre 4 » sont prudents, et ainsi de suite.
REPARTITION_DES_PROFILS = {
    "prudent": 4,
    "dépensier": 3,
    "absentéiste": 3,
}

# Nombre de tokens que possède chaque membre au départ.
TOKENS_PAR_MEMBRE = 100

# Un prudent vote « oui » si le coût est au plus ce pourcentage de la trésorerie.
SEUIL_PRUDENT_POURCENT = 30

# Un absentéiste vote avec « une chance sur » ce nombre.
CHANCE_DE_VOTER_ABSENTEISTE = 3


# =====================================================================
# TRÉSORERIE ET DURÉE DE LA PARTIE
# =====================================================================

# Crédits dans la caisse commune au début de la partie.
TRESORERIE_DE_DEPART = 500

# Crédits retirés de la caisse à la fin de chaque tour.
FRAIS_FIXES = 30

# Nombre de tours au bout duquel la partie s'arrête.
NOMBRE_DE_TOURS_MAX = 30

# Trésorerie à atteindre pour gagner.
OBJECTIF_DE_VICTOIRE = 2000


# =====================================================================
# RÈGLES DE VOTE
# =====================================================================

# Quorum en pourcentage des tokens : participation minimale pour que le vote compte.
QUORUM_POURCENT = 40

# Majorité en pourcentage : les « oui » doivent faire STRICTEMENT plus que ce nombre.
MAJORITE_POURCENT = 50


# =====================================================================
# BÂTIMENTS
# =====================================================================

# Pour chaque bâtiment : son coût, et la liste des revenus possibles par tour.
# S'il y a plusieurs revenus possibles, on en tire un au hasard à chaque tour.
BATIMENTS = {
    "Ferme": {"cout": 100, "revenus_possibles": [20]},
    "Atelier": {"cout": 200, "revenus_possibles": [45]},
    "Marché": {"cout": 150, "revenus_possibles": [0, 80]},
}


# =====================================================================
# HASARD
# =====================================================================

# Graine aléatoire : avec la même graine, le hasard donne toujours la même partie.
GRAINE_ALEATOIRE = 42
