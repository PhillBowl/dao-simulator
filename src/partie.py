# Le modèle de la partie : l'état de la DAO et le déroulement des tours.
# Ce fichier n'affiche rien : il produit un journal de données,
# que d'autres fichiers mettent en forme (terminal aujourd'hui, rapport HTML demain).

# Le module "random" sert à tirer des choses au hasard.
import random

# On lit les réglages, et on utilise les membres pour leur demander leur vote.
import reglages
import membres


# Les résultats possibles d'une proposition.
RESULTAT_CONSTRUITE = "adoptée, construite"
RESULTAT_FONDS_INSUFFISANTS = "adoptée, non construite (fonds insuffisants)"
RESULTAT_REJETEE = "rejetée"
RESULTAT_SANS_QUORUM = "rejetée faute de quorum"

# Les issues possibles d'une partie.
ISSUE_VICTOIRE = "victoire"
ISSUE_DEFAITE = "défaite"


# =====================================================================
# ÉTAT DE LA DAO
# =====================================================================

def creer_etat_dao():
    """Crée l'état de départ de la DAO : tour, trésorerie, bâtiments construits."""
    return {
        "tour": 0,
        "tresorerie": reglages.TRESORERIE_DE_DEPART,
        # Chaque bâtiment construit sera une fiche : son nom et son tour de construction.
        "batiments": [],
    }


# =====================================================================
# ÉTAPE 1 : PROPOSITION
# =====================================================================

def tirer_proposition(liste_membres):
    """Tire au hasard un auteur parmi les membres et un bâtiment à construire."""
    # L'auteur est tiré au hasard, quel que soit son profil.
    auteur = random.choice(liste_membres)
    # On fait la liste des noms de bâtiments, puis on en tire un.
    noms_des_batiments = list(reglages.BATIMENTS)
    nom_du_batiment = random.choice(noms_des_batiments)
    # La proposition rassemble ce dont les membres ont besoin pour voter.
    return {
        "auteur": auteur["nom"],
        "profil_auteur": auteur["profil"],
        "batiment": nom_du_batiment,
        "cout": reglages.BATIMENTS[nom_du_batiment]["cout"],
    }


# =====================================================================
# ÉTAPE 2 : VOTE
# =====================================================================

def recueillir_votes(liste_membres, proposition, etat_dao):
    """Pose la même question à chaque membre et note sa réponse."""
    votes = []
    # Chaque membre répond selon son profil ; la partie ne sait pas comment il décide.
    for membre in liste_membres:
        reponse = membres.demander_vote(membre, proposition, etat_dao)
        # On garde le profil et les tokens avec le vote, pour les analyses futures.
        votes.append({
            "nom": membre["nom"],
            "profil": membre["profil"],
            "tokens": membre["tokens"],
            "vote": reponse,
        })
    return votes


# =====================================================================
# ÉTAPE 3 : DÉPOUILLEMENT
# =====================================================================

def compter_tokens(votes, choix):
    """Additionne les tokens des membres qui ont fait un certain choix."""
    total = 0
    for vote in votes:
        if vote["vote"] == choix:
            total = total + vote["tokens"]
    return total


def compter_membres(votes, choix):
    """Compte les membres qui ont fait un certain choix."""
    total = 0
    for vote in votes:
        if vote["vote"] == choix:
            total = total + 1
    return total


def calculer_pourcentage(partie, total):
    """Calcule quel pourcentage « partie » représente dans « total »."""
    # On évite de diviser par zéro, ce qui ferait planter le programme.
    if total == 0:
        return 0
    return partie * 100 / total


def depouiller(votes):
    """Compte les votes, vérifie le quorum et la majorité."""
    # Tokens et nombre de membres pour chaque réponse.
    tokens_oui = compter_tokens(votes, membres.OUI)
    tokens_non = compter_tokens(votes, membres.NON)
    membres_oui = compter_membres(votes, membres.OUI)
    membres_non = compter_membres(votes, membres.NON)

    # Le total des tokens existants, votants ou non.
    tokens_total = 0
    for vote in votes:
        tokens_total = tokens_total + vote["tokens"]

    # Participation : part des tokens qui ont voté (oui + non).
    tokens_exprimes = tokens_oui + tokens_non
    participation = calculer_pourcentage(tokens_exprimes, tokens_total)
    quorum_atteint = participation >= reglages.QUORUM_POURCENT

    # Majorité : les oui doivent faire STRICTEMENT plus que le seuil ; l'égalité rejette.
    pourcentage_oui = calculer_pourcentage(tokens_oui, tokens_exprimes)
    majorite_atteinte = pourcentage_oui > reglages.MAJORITE_POURCENT

    return {
        "tokens_oui": tokens_oui,
        "tokens_non": tokens_non,
        "membres_oui": membres_oui,
        "membres_non": membres_non,
        "participation": participation,
        "quorum_atteint": quorum_atteint,
        "adoptee": quorum_atteint and majorite_atteinte,
    }


# =====================================================================
# ÉTAPE 4 : EXÉCUTION
# =====================================================================

def executer(proposition, depouillement, etat_dao):
    """Construit le bâtiment si la proposition est adoptée et que la caisse suffit."""
    # Sans quorum, la proposition tombe sans même regarder la majorité.
    if not depouillement["quorum_atteint"]:
        return RESULTAT_SANS_QUORUM
    # Quorum atteint mais pas de majorité : rejet.
    if not depouillement["adoptee"]:
        return RESULTAT_REJETEE
    # Adoptée, mais la trésorerie ne couvre pas le coût : rien n'est construit.
    if etat_dao["tresorerie"] < proposition["cout"]:
        return RESULTAT_FONDS_INSUFFISANTS
    # Adoptée et financée : on paie et on ajoute le bâtiment à la DAO.
    etat_dao["tresorerie"] = etat_dao["tresorerie"] - proposition["cout"]
    etat_dao["batiments"].append({
        "nom": proposition["batiment"],
        "tour_de_construction": etat_dao["tour"],
    })
    return RESULTAT_CONSTRUITE


# =====================================================================
# ÉTAPES 5 ET 6 : REVENUS ET FRAIS
# =====================================================================

def tirer_revenu(nom_du_batiment):
    """Donne le revenu d'un bâtiment pour ce tour (tiré au hasard pour le Marché)."""
    revenus_possibles = reglages.BATIMENTS[nom_du_batiment]["revenus_possibles"]
    # Un seul revenu possible : pas de hasard.
    if len(revenus_possibles) == 1:
        return revenus_possibles[0]
    # Plusieurs revenus possibles : on en tire un.
    return random.choice(revenus_possibles)


def encaisser_revenus(etat_dao):
    """Ajoute à la caisse le revenu des bâtiments construits lors d'un tour précédent."""
    total = 0
    for batiment in etat_dao["batiments"]:
        # Un bâtiment construit ce tour-ci ne rapporte qu'à partir du tour suivant.
        if batiment["tour_de_construction"] < etat_dao["tour"]:
            total = total + tirer_revenu(batiment["nom"])
    etat_dao["tresorerie"] = etat_dao["tresorerie"] + total
    return total


def payer_frais(etat_dao):
    """Retire les frais fixes de la caisse."""
    etat_dao["tresorerie"] = etat_dao["tresorerie"] - reglages.FRAIS_FIXES


# =====================================================================
# ÉTAPE 7 : VÉRIFICATION
# =====================================================================

def verifier_fin(etat_dao):
    """Dit si la partie est finie : renvoie l'issue et sa cause, ou None si on continue."""
    tresorerie = etat_dao["tresorerie"]
    # Victoire : l'objectif est atteint (y compris au dernier tour).
    if tresorerie >= reglages.OBJECTIF_DE_VICTOIRE:
        cause = ("la trésorerie a atteint l'objectif de "
                 + str(reglages.OBJECTIF_DE_VICTOIRE) + " crédits")
        return {"issue": ISSUE_VICTOIRE, "cause": cause}
    # Défaite : la caisse est passée sous zéro (zéro tout juste ne suffit pas).
    if tresorerie < 0:
        return {"issue": ISSUE_DEFAITE, "cause": "la trésorerie est passée sous zéro"}
    # Défaite : le dernier tour est joué sans victoire.
    if etat_dao["tour"] >= reglages.NOMBRE_DE_TOURS_MAX:
        cause = ("le tour " + str(reglages.NOMBRE_DE_TOURS_MAX)
                 + " est atteint sans victoire")
        return {"issue": ISSUE_DEFAITE, "cause": cause}
    # Sinon, la partie continue.
    return None


# =====================================================================
# LA PARTIE COMPLÈTE
# =====================================================================

def jouer_tour(liste_membres, etat_dao):
    """Joue les 7 étapes d'un tour et renvoie ce qui s'est passé."""
    # On passe au tour suivant.
    etat_dao["tour"] = etat_dao["tour"] + 1
    # Étapes 1 à 3 : proposition, vote, dépouillement.
    proposition = tirer_proposition(liste_membres)
    votes = recueillir_votes(liste_membres, proposition, etat_dao)
    depouillement = depouiller(votes)
    # Étape 4 : exécution.
    resultat = executer(proposition, depouillement, etat_dao)
    # Étapes 5 et 6 : revenus puis frais.
    revenus = encaisser_revenus(etat_dao)
    payer_frais(etat_dao)
    # On renvoie une fiche qui résume le tour.
    return {
        "tour": etat_dao["tour"],
        "proposition": proposition,
        "votes": votes,
        "depouillement": depouillement,
        "resultat": resultat,
        "revenus": revenus,
        "frais": reglages.FRAIS_FIXES,
        "tresorerie_fin_de_tour": etat_dao["tresorerie"],
    }


def jouer_partie():
    """Joue une partie jusqu'à la victoire ou la défaite, et renvoie ses données."""
    # Mise en place : les membres et l'état de départ de la DAO.
    liste_membres = membres.creer_membres()
    etat_dao = creer_etat_dao()
    journal = []

    # On joue des tours tant que la vérification ne déclare pas la fin.
    fin = None
    while fin is None:
        fiche_du_tour = jouer_tour(liste_membres, etat_dao)
        journal.append(fiche_du_tour)
        # Étape 7 : vérification sur la trésorerie de fin de tour.
        fin = verifier_fin(etat_dao)

    # Les données de la partie, prêtes à être affichées (ou mises dans un rapport).
    return {
        "journal": journal,
        "issue": fin["issue"],
        "cause": fin["cause"],
        "tours_joues": etat_dao["tour"],
        "tresorerie_finale": etat_dao["tresorerie"],
    }
