# Les membres de la DAO : leur création et leur façon de voter.
# Un membre lit l'état de la DAO mais ne le modifie jamais.
# Tous les profils répondent à la même question :
# « voici la proposition et l'état de la DAO, que votes-tu ? »

# Le module "random" sert à tirer des choses au hasard.
import random

# On lit les réglages de la partie.
import reglages


# Les trois réponses possibles d'un membre.
OUI = "oui"
NON = "non"
NE_VOTE_PAS = "ne vote pas"


def creer_membres():
    """Crée la liste des membres, chacun avec un nom, des tokens et un profil."""
    # On commence avec une liste vide et un compteur pour numéroter les membres.
    membres = []
    numero = 1
    # Pour chaque profil, on crée le nombre de membres prévu dans les réglages.
    for profil in reglages.REPARTITION_DES_PROFILS:
        nombre = reglages.REPARTITION_DES_PROFILS[profil]
        for _ in range(nombre):
            # Un membre est un dictionnaire : une fiche avec des champs nommés.
            membre = {
                "nom": "Membre " + str(numero),
                "tokens": reglages.TOKENS_PAR_MEMBRE,
                "profil": profil,
            }
            membres.append(membre)
            numero = numero + 1
    # On renvoie la liste complète.
    return membres


def voter_prudent(proposition, etat_dao):
    """Oui si le coût ne dépasse pas le seuil prudent de la trésorerie, sinon non."""
    # Montant maximal qu'un prudent accepte de dépenser (30 % de la trésorerie).
    montant_acceptable = etat_dao["tresorerie"] * reglages.SEUIL_PRUDENT_POURCENT / 100
    # On compare le coût du bâtiment proposé à ce montant.
    if proposition["cout"] <= montant_acceptable:
        return OUI
    return NON


def voter_depensier(proposition, etat_dao):
    """Toujours oui, quels que soient la proposition et l'état de la DAO."""
    return OUI


def voter_absenteiste(proposition, etat_dao):
    """Vote une fois sur trois ; s'il vote, oui ou non à pile ou face."""
    # On tire un nombre entre 1 et 3 : seul le 1 fait voter le membre.
    tirage = random.randint(1, reglages.CHANCE_DE_VOTER_ABSENTEISTE)
    if tirage != 1:
        return NE_VOTE_PAS
    # Il vote : pile ou face entre oui et non.
    return random.choice([OUI, NON])


def demander_vote(membre, proposition, etat_dao):
    """Pose la question commune à un membre et renvoie sa réponse."""
    # On passe la main à la règle qui correspond au profil du membre.
    profil = membre["profil"]
    if profil == "prudent":
        return voter_prudent(proposition, etat_dao)
    if profil == "dépensier":
        return voter_depensier(proposition, etat_dao)
    if profil == "absentéiste":
        return voter_absenteiste(proposition, etat_dao)
    # Un profil inconnu est une erreur de réglage : on arrête avec un message clair.
    raise ValueError("Profil inconnu : " + profil)
