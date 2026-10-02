# Simulateur d'un vote de DAO (organisation autonome décentralisée).
# Ce programme simule un seul vote et affiche le résultat.

# On importe le module "random" de Python, qui sert à tirer des choses au hasard.
import random


# =====================================================================
# RÉGLAGES : modifie ces valeurs pour changer la simulation
# =====================================================================

# Nombre de membres dans la DAO.
NOMBRE_DE_MEMBRES = 10

# Nombre de tokens que possède chaque membre au départ.
TOKENS_PAR_MEMBRE = 100

# Quorum en pourcentage : participation minimale pour que le vote compte.
QUORUM_POURCENT = 400

# Majorité en pourcentage : les "oui" doivent faire STRICTEMENT plus que ce nombre.
MAJORITE_POURCENT = 50

# Graine aléatoire : avec la même graine, le hasard donne toujours le même résultat.
GRAINE_ALEATOIRE = 42

# Les trois choix possibles pour un membre.
CHOIX_POSSIBLES = ["oui", "non", "ne vote pas"]


# =====================================================================
# FONCTIONS
# =====================================================================

def creer_membres():
    """Crée la liste des membres, chacun avec un nom et des tokens."""
    # On commence avec une liste vide.
    membres = []
    # On répète pour chaque numéro, de 1 jusqu'au nombre de membres inclus.
    for numero in range(1, NOMBRE_DE_MEMBRES + 1):
        # Un membre est un dictionnaire : un petit "fichier" avec des champs nommés.
        membre = {
            "nom": "Membre " + str(numero),
            "tokens": TOKENS_PAR_MEMBRE,
        }
        # On ajoute ce membre à la liste.
        membres.append(membre)
    # On renvoie la liste complète.
    return membres


def faire_voter(membres):
    """Fait choisir au hasard un vote pour chaque membre."""
    # Pour chaque membre de la liste...
    for membre in membres:
        # ...on tire un choix au hasard parmi les trois (une chance sur trois chacun).
        membre["vote"] = random.choice(CHOIX_POSSIBLES)


def compter_tokens(membres, choix):
    """Additionne les tokens des membres qui ont fait un certain choix."""
    # Le compteur part de zéro.
    total = 0
    # On regarde chaque membre.
    for membre in membres:
        # Si son vote correspond au choix recherché, on ajoute ses tokens.
        if membre["vote"] == choix:
            total = total + membre["tokens"]
    # On renvoie la somme.
    return total


def calculer_pourcentage(partie, total):
    """Calcule quel pourcentage "partie" représente dans "total"."""
    # On évite de diviser par zéro, ce qui ferait planter le programme.
    if total == 0:
        return 0
    # Règle de trois classique.
    return partie * 100 / total


def quorum_atteint(participation):
    """Indique si la participation est suffisante (vrai ou faux)."""
    # Le quorum est atteint si la participation est au moins égale au seuil.
    return participation >= QUORUM_POURCENT


def proposition_adoptee(pourcentage_oui, quorum_ok):
    """Décide si la proposition est adoptée (vrai ou faux)."""
    # Sans quorum, la proposition est rejetée, quoi qu'il arrive.
    if not quorum_ok:
        return False
    # Sinon, il faut STRICTEMENT plus que la majorité (une égalité ne suffit pas).
    return pourcentage_oui > MAJORITE_POURCENT


def afficher_votes(membres):
    """Affiche le vote de chaque membre."""
    # On affiche le titre.
    print("=== Vote de la DAO ===")
    # On affiche une ligne par membre.
    for membre in membres:
        # Un membre qui ne vote pas n'engage pas ses tokens.
        if membre["vote"] == "ne vote pas":
            print(membre["nom"] + " : ne vote pas")
        # Sinon, on indique son vote et ses tokens.
        else:
            print(membre["nom"] + " : " + membre["vote"]
                  + " (" + str(membre["tokens"]) + " tokens)")


def afficher_resultat(participation, quorum_ok, tokens_oui, tokens_non, adoptee):
    """Affiche la participation, le décompte des voix et le résultat final."""
    # On choisit le texte à afficher selon que le quorum est atteint ou non.
    if quorum_ok:
        texte_quorum = "quorum atteint"
    else:
        texte_quorum = "quorum non atteint"
    # On affiche la participation (arrondie à l'entier avec round).
    print("Participation : " + str(round(participation)) + " % (quorum : "
          + str(QUORUM_POURCENT) + " %) → " + texte_quorum)

    # Les votes exprimés sont les "oui" plus les "non".
    votes_exprimes = tokens_oui + tokens_non
    # On calcule la part des "oui" et des "non" parmi les votes exprimés.
    pourcentage_oui = calculer_pourcentage(tokens_oui, votes_exprimes)
    pourcentage_non = calculer_pourcentage(tokens_non, votes_exprimes)
    # On affiche le décompte.
    print("Oui : " + str(tokens_oui) + " tokens (" + str(round(pourcentage_oui)) + " %)"
          + " — Non : " + str(tokens_non) + " tokens (" + str(round(pourcentage_non)) + " %)")

    # On affiche le résultat final.
    if adoptee:
        print("Résultat : proposition ADOPTÉE")
    else:
        print("Résultat : proposition REJETÉE")


def main():
    """Fonction principale : enchaîne toutes les étapes du vote."""
    # 1. On fixe la graine pour que le hasard soit toujours le même.
    random.seed(GRAINE_ALEATOIRE)

    # 2. On crée les membres, puis on les fait voter.
    membres = creer_membres()
    faire_voter(membres)

    # 3. On compte les tokens pour chaque type de vote.
    tokens_oui = compter_tokens(membres, "oui")
    tokens_non = compter_tokens(membres, "non")
    # Le total des tokens existants, votants ou non.
    tokens_total = NOMBRE_DE_MEMBRES * TOKENS_PAR_MEMBRE

    # 4. On calcule la participation et on vérifie le quorum.
    participation = calculer_pourcentage(tokens_oui + tokens_non, tokens_total)
    quorum_ok = quorum_atteint(participation)

    # 5. On calcule la part des "oui" parmi les votes exprimés et on décide.
    pourcentage_oui = calculer_pourcentage(tokens_oui, tokens_oui + tokens_non)
    adoptee = proposition_adoptee(pourcentage_oui, quorum_ok)

    # 6. On affiche tout.
    afficher_votes(membres)
    afficher_resultat(participation, quorum_ok, tokens_oui, tokens_non, adoptee)


# Cette ligne lance main() seulement si on exécute ce fichier directement.
if __name__ == "__main__":
    main()
