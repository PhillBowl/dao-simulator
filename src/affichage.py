# Affichage d'une partie dans le terminal.
# Ce fichier lit les données produites par la partie ; il ne change aucune règle.


def formater_ligne_de_tour(fiche):
    """Construit la ligne de texte qui résume un tour."""
    proposition = fiche["proposition"]
    depouillement = fiche["depouillement"]

    # Numéro du tour, aligné sur deux caractères (« 1 » devient «  1 »).
    texte_tour = "Tour " + str(fiche["tour"]).rjust(2)

    # Auteur, son profil, et le bâtiment proposé avec son coût.
    texte_proposition = (proposition["auteur"] + " (" + proposition["profil_auteur"] + ")"
                         + " propose " + proposition["batiment"]
                         + " (" + str(proposition["cout"]) + ")")

    # Votes : nombre de membres et, entre parenthèses, leurs tokens.
    texte_votes = ("oui " + str(depouillement["membres_oui"])
                   + " (" + str(depouillement["tokens_oui"]) + ")"
                   + " · non " + str(depouillement["membres_non"])
                   + " (" + str(depouillement["tokens_non"]) + ")"
                   + " · participation " + str(round(depouillement["participation"])) + " %")

    # Trésorerie de fin de tour.
    texte_tresorerie = "trésorerie " + str(fiche["tresorerie_fin_de_tour"])

    # On assemble les morceaux, séparés par des barres verticales.
    return (texte_tour + " | " + texte_proposition + " | " + texte_votes
            + " | " + fiche["resultat"] + " | " + texte_tresorerie)


def afficher_debut(graine):
    """Affiche le titre de la partie."""
    print("=== Partie de DAO (graine " + str(graine) + ") ===")


def afficher_journal(donnees_partie):
    """Affiche une ligne par tour joué."""
    for fiche in donnees_partie["journal"]:
        print(formater_ligne_de_tour(fiche))


def afficher_resultat(donnees_partie):
    """Affiche le résultat final, sa cause et le nombre de tours joués."""
    print("=== Fin de la partie ===")
    print("Résultat : " + donnees_partie["issue"].upper())
    print("Cause : " + donnees_partie["cause"]
          + " (trésorerie finale : " + str(donnees_partie["tresorerie_finale"]) + ")")
    print("Tours joués : " + str(donnees_partie["tours_joues"]))
