# Tests des membres et de leurs profils de vote (spec V1, tableaux « Départ » et « Profils »).
# Chaque valeur attendue est calculée à partir des règles de la spec, pas du code.
# Commande : python3 -m unittest discover -s tests -v

import os
import random
import sys
import unittest

# On indique à Python où trouver le code du simulateur (le dossier src/).
DOSSIER_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.insert(0, DOSSIER_SRC)

import membres
import partie


# Graine fixe : les tests de l'absentéiste donnent toujours le même résultat.
GRAINE_ALEATOIRE = 42

# Nombre de fois où l'on interroge un absentéiste pour mesurer son comportement.
NOMBRE_DE_TIRAGES = 3000

# « Une chance sur trois » de voter : environ 1000 votants sur 3000, fourchette large.
VOTANTS_MINIMUM = 900
VOTANTS_MAXIMUM = 1100

# « Pile ou face » entre oui et non : environ 50 % de oui parmi les votants.
POURCENT_OUI_MINIMUM = 40
POURCENT_OUI_MAXIMUM = 60

# Coûts des bâtiments, tableau « Bâtiments » de la spec.
COUT_FERME = 100
COUT_MARCHE = 150
COUT_ATELIER = 200


def construire_proposition(batiment, cout, auteur="Membre 1", profil_auteur="dépensier"):
    """Fabrique une proposition de bâtiment."""
    return {
        "auteur": auteur,
        "profil_auteur": profil_auteur,
        "batiment": batiment,
        "cout": cout,
    }


def construire_etat(tresorerie):
    """Fabrique un état de la DAO avec la trésorerie voulue."""
    etat_dao = partie.creer_etat_dao()
    etat_dao["tresorerie"] = tresorerie
    return etat_dao


def construire_membre(profil):
    """Fabrique un membre seul, du profil voulu."""
    return {"nom": "Membre test", "tokens": 100, "profil": profil}


def compter_profil(liste_membres, profil):
    """Compte les membres d'un profil donné."""
    total = 0
    for membre in liste_membres:
        if membre["profil"] == profil:
            total = total + 1
    return total


class TestCreationDesMembres(unittest.TestCase):
    """Règle : 10 membres nommés « Membre 1 » à « Membre 10 », 100 tokens, 4 / 3 / 3."""

    def test_C1_creation_des_membres(self):
        liste_membres = membres.creer_membres()
        self.assertEqual(len(liste_membres), 10,
                         "C1 : la spec prévoit 10 membres.")
        # Les noms vont de « Membre 1 » à « Membre 10 ».
        noms_attendus = []
        for numero in range(1, 11):
            noms_attendus.append("Membre " + str(numero))
        noms_obtenus = []
        for membre in liste_membres:
            noms_obtenus.append(membre["nom"])
        self.assertEqual(noms_obtenus, noms_attendus,
                         "C1 : les membres doivent s'appeler « Membre 1 » à « Membre 10 ».")
        # Chaque membre a 100 tokens.
        for membre in liste_membres:
            self.assertEqual(membre["tokens"], 100,
                             "C1 : " + membre["nom"] + " doit avoir 100 tokens.")
        # Répartition des profils.
        self.assertEqual(compter_profil(liste_membres, "prudent"), 4,
                         "C1 : la spec prévoit 4 prudents.")
        self.assertEqual(compter_profil(liste_membres, "dépensier"), 3,
                         "C1 : la spec prévoit 3 dépensiers.")
        self.assertEqual(compter_profil(liste_membres, "absentéiste"), 3,
                         "C1 : la spec prévoit 3 absentéistes.")


class TestPrudent(unittest.TestCase):
    """Règle : oui si le coût est inférieur ou égal à 30 % de la trésorerie ; sinon non."""

    def demander_au_prudent(self, cout, tresorerie):
        """Pose la question à un prudent et renvoie sa réponse."""
        proposition = construire_proposition("Bâtiment", cout)
        return membres.demander_vote(construire_membre("prudent"), proposition,
                                     construire_etat(tresorerie))

    def test_C2_cout_sous_le_seuil(self):
        self.assertEqual(self.demander_au_prudent(COUT_FERME, 500), membres.OUI,
                         "C2 : 30 % de 500 = 150 ; une Ferme à 100 est en dessous : oui attendu.")

    def test_C3_cout_egal_au_seuil(self):
        self.assertEqual(self.demander_au_prudent(COUT_MARCHE, 500), membres.OUI,
                         "C3 : 30 % de 500 = 150 ; un Marché à 150 est égal au seuil. "
                         "La spec dit « inférieur ou égal » : oui attendu.")

    def test_C4_cout_au_dessus_du_seuil(self):
        self.assertEqual(self.demander_au_prudent(COUT_ATELIER, 500), membres.NON,
                         "C4 : 30 % de 500 = 150 ; un Atelier à 200 dépasse : non attendu.")

    def test_C5_seuil_non_entier(self):
        self.assertEqual(self.demander_au_prudent(COUT_FERME, 333), membres.NON,
                         "C5 : 30 % de 333 = 99,9 ; une Ferme à 100 dépasse : non attendu.")

    def test_C6_tresorerie_vide(self):
        self.assertEqual(self.demander_au_prudent(COUT_FERME, 0), membres.NON,
                         "C6 : 30 % de 0 = 0 ; une Ferme à 100 dépasse : non attendu.")


class TestDepensier(unittest.TestCase):
    """Règle : toujours oui."""

    def test_C7_toujours_oui(self):
        proposition = construire_proposition("Atelier", COUT_ATELIER)
        for tresorerie in [500, 0]:
            reponse = membres.demander_vote(construire_membre("dépensier"), proposition,
                                            construire_etat(tresorerie))
            self.assertEqual(reponse, membres.OUI,
                             "C7 : un dépensier vote toujours oui "
                             "(Atelier, trésorerie " + str(tresorerie) + ").")


class TestAuteur(unittest.TestCase):
    """Règle : l'auteur d'une proposition vote selon son profil, comme les autres membres."""

    def test_C8_auteur_prudent_vote_selon_son_profil(self):
        liste_membres = membres.creer_membres()
        # On choisit comme auteur le premier prudent de la liste.
        auteur = None
        for membre in liste_membres:
            if membre["profil"] == "prudent" and auteur is None:
                auteur = membre
        proposition = construire_proposition("Atelier", COUT_ATELIER,
                                             auteur["nom"], auteur["profil"])
        random.seed(GRAINE_ALEATOIRE)
        votes = partie.recueillir_votes(liste_membres, proposition, construire_etat(500))
        # On retrouve le vote de l'auteur.
        vote_auteur = None
        for vote in votes:
            if vote["nom"] == auteur["nom"]:
                vote_auteur = vote["vote"]
        self.assertEqual(vote_auteur, membres.NON,
                         "C8 : l'auteur est prudent et propose un Atelier à 200 "
                         "avec 500 en caisse (seuil 150). Il vote selon son profil : non attendu.")


class TestAbsenteiste(unittest.TestCase):
    """Règle : vote avec une chance sur trois ; s'il vote, oui ou non à pile ou face.
    Graine fixe et grand nombre de tirages : le résultat est toujours le même."""

    def interroger_absenteiste(self, tresorerie, cout):
        """Pose la même question NOMBRE_DE_TIRAGES fois et renvoie toutes les réponses."""
        random.seed(GRAINE_ALEATOIRE)
        proposition = construire_proposition("Bâtiment", cout)
        etat_dao = construire_etat(tresorerie)
        reponses = []
        for _ in range(NOMBRE_DE_TIRAGES):
            reponses.append(membres.demander_vote(construire_membre("absentéiste"),
                                                  proposition, etat_dao))
        return reponses

    def test_C9a_reponses_possibles(self):
        reponses = self.interroger_absenteiste(500, COUT_FERME)
        for reponse in reponses:
            self.assertIn(reponse, [membres.OUI, membres.NON, membres.NE_VOTE_PAS],
                          "C9a : un absentéiste répond oui, non ou ne vote pas, rien d'autre.")

    def test_C9b_une_chance_sur_trois_de_voter(self):
        reponses = self.interroger_absenteiste(500, COUT_FERME)
        votants = NOMBRE_DE_TIRAGES - reponses.count(membres.NE_VOTE_PAS)
        self.assertTrue(VOTANTS_MINIMUM <= votants <= VOTANTS_MAXIMUM,
                        "C9b : « une chance sur trois » sur 3000 tirages donne environ 1000 votants "
                        "(attendu entre " + str(VOTANTS_MINIMUM) + " et " + str(VOTANTS_MAXIMUM)
                        + "), obtenu " + str(votants) + ".")

    def test_C9c_pile_ou_face_entre_oui_et_non(self):
        reponses = self.interroger_absenteiste(500, COUT_FERME)
        nombre_oui = reponses.count(membres.OUI)
        votants = nombre_oui + reponses.count(membres.NON)
        pourcent_oui = nombre_oui * 100 / votants
        self.assertTrue(POURCENT_OUI_MINIMUM <= pourcent_oui <= POURCENT_OUI_MAXIMUM,
                        "C9c : « pile ou face » donne environ 50 % de oui parmi les votants "
                        "(attendu entre " + str(POURCENT_OUI_MINIMUM) + " et "
                        + str(POURCENT_OUI_MAXIMUM) + " %), obtenu "
                        + str(round(pourcent_oui, 1)) + " %.")

    def test_C9d_ne_regarde_pas_la_tresorerie(self):
        reponses = self.interroger_absenteiste(0, COUT_ATELIER)
        self.assertIn(membres.OUI, reponses,
                      "C9d : avec 0 en caisse et un Atelier à 200, un absentéiste "
                      "doit quand même voter oui de temps en temps : "
                      "son vote ne dépend pas de la trésorerie.")


if __name__ == "__main__":
    unittest.main()
