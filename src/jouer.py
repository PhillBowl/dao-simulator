# Point d'entrée : lance une partie complète de DAO et l'affiche dans le terminal.
# Commande : python3 src/jouer.py

# Le module "random" sert à tirer des choses au hasard.
import random

# Les réglages, le modèle de la partie et son affichage.
import reglages
import partie
import affichage


def main():
    """Fonction principale : fixe la graine, joue la partie, l'affiche."""
    # 1. On fixe la graine pour que le hasard donne toujours la même partie.
    random.seed(reglages.GRAINE_ALEATOIRE)

    # 2. On joue la partie : elle renvoie des données, sans rien afficher.
    donnees_partie = partie.jouer_partie()

    # 3. On affiche ces données.
    affichage.afficher_debut(reglages.GRAINE_ALEATOIRE)
    affichage.afficher_journal(donnees_partie)
    affichage.afficher_resultat(donnees_partie)


# Cette ligne lance main() seulement si on exécute ce fichier directement.
if __name__ == "__main__":
    main()
