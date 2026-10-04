# Tests du dépouillement : quorum et majorité (spec V1, « Déroulement d'un tour », étape 3).
# Chaque valeur attendue est calculée à partir des règles de la spec, pas du code.
# Commande : python3 -m unittest discover -s tests -v

import os
import sys
import unittest

# On indique à Python où trouver le code du simulateur (le dossier src/).
DOSSIER_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.insert(0, DOSSIER_SRC)

import membres
import partie


# Valeurs de la spec, tableau « Départ » : 10 membres de 100 tokens, soit 1000 tokens.
NOMBRE_DE_MEMBRES = 10
TOKENS_PAR_MEMBRE = 100


def construire_votes(nombre_oui, nombre_non):
    """Fabrique les votes des 10 membres : des oui, des non, et le reste ne vote pas."""
    votes = []
    for numero in range(1, NOMBRE_DE_MEMBRES + 1):
        # Les premiers votent oui, les suivants non, les derniers ne votent pas.
        if numero <= nombre_oui:
            choix = membres.OUI
        elif numero <= nombre_oui + nombre_non:
            choix = membres.NON
        else:
            choix = membres.NE_VOTE_PAS
        votes.append({
            "nom": "Membre " + str(numero),
            "profil": "dépensier",
            "tokens": TOKENS_PAR_MEMBRE,
            "vote": choix,
        })
    return votes


def construire_proposition():
    """Fabrique une proposition de Ferme (coût 100), utile pour appeler l'exécution."""
    return {
        "auteur": "Membre 1",
        "profil_auteur": "dépensier",
        "batiment": "Ferme",
        "cout": 100,
    }


class TestQuorum(unittest.TestCase):
    """Règle : quorum atteint si les tokens des votants (oui + non) font au moins 40 % du total."""

    def test_A1_quorum_atteint(self):
        resultat = partie.depouiller(construire_votes(3, 2))
        self.assertTrue(resultat["quorum_atteint"],
                        "A1 : 5 votants = 500 tokens sur 1000 = 50 %, "
                        "au moins 40 % : le quorum doit être atteint.")

    def test_A2_quorum_non_atteint(self):
        votes = construire_votes(3, 0)
        resultat = partie.depouiller(votes)
        self.assertFalse(resultat["quorum_atteint"],
                         "A2 : 3 votants = 300 tokens sur 1000 = 30 %, "
                         "moins de 40 % : le quorum ne doit pas être atteint.")
        self.assertFalse(resultat["adoptee"],
                         "A2 : sans quorum, la proposition ne peut pas être adoptée, "
                         "même avec 100 % de oui.")
        # Le résultat de la proposition doit être « rejetée faute de quorum ».
        etat_dao = partie.creer_etat_dao()
        resultat_final = partie.executer(construire_proposition(), resultat, etat_dao)
        self.assertEqual(resultat_final, partie.RESULTAT_SANS_QUORUM,
                         "A2 : sans quorum, le résultat doit être « rejetée faute de quorum ».")

    def test_A3_quorum_exactement_au_seuil(self):
        resultat = partie.depouiller(construire_votes(2, 2))
        self.assertTrue(resultat["quorum_atteint"],
                        "A3 : 4 votants = 400 tokens sur 1000 = 40 % exactement. "
                        "La spec dit « au moins le quorum » : il doit être atteint.")

    def test_A4_personne_ne_vote(self):
        resultat = partie.depouiller(construire_votes(0, 0))
        self.assertFalse(resultat["quorum_atteint"],
                         "A4 : aucun votant = 0 % : le quorum ne doit pas être atteint.")
        self.assertFalse(resultat["adoptee"],
                         "A4 : aucun votant : la proposition ne peut pas être adoptée.")


class TestMajorite(unittest.TestCase):
    """Règle : adoption si les oui dépassent strictement 50 % des votes exprimés ; égalité = rejet."""

    def test_B1_majorite_adoptee(self):
        resultat = partie.depouiller(construire_votes(6, 4))
        self.assertTrue(resultat["adoptee"],
                        "B1 : 6 oui contre 4 non = 60 % des exprimés, "
                        "strictement plus de 50 % : la proposition doit être adoptée.")

    def test_B2_majorite_rejetee(self):
        resultat = partie.depouiller(construire_votes(4, 6))
        self.assertFalse(resultat["adoptee"],
                         "B2 : 4 oui contre 6 non = 40 % des exprimés : "
                         "la proposition doit être rejetée.")
        # Le quorum est atteint (100 %) : c'est un rejet simple, pas « faute de quorum ».
        etat_dao = partie.creer_etat_dao()
        resultat_final = partie.executer(construire_proposition(), resultat, etat_dao)
        self.assertEqual(resultat_final, partie.RESULTAT_REJETEE,
                         "B2 : quorum atteint mais majorité manquée : "
                         "le résultat doit être « rejetée », pas « faute de quorum ».")

    def test_B3_egalite(self):
        resultat = partie.depouiller(construire_votes(5, 5))
        self.assertFalse(resultat["adoptee"],
                         "B3 : 5 oui contre 5 non = 50 %, pas strictement plus. "
                         "La spec dit « une égalité entraîne le rejet ».")

    def test_B4_egalite_au_seuil_du_quorum(self):
        resultat = partie.depouiller(construire_votes(2, 2))
        self.assertTrue(resultat["quorum_atteint"],
                        "B4 : 4 votants = 40 % : le quorum doit être atteint.")
        self.assertFalse(resultat["adoptee"],
                         "B4 : 2 oui contre 2 non = 50 % des exprimés : "
                         "l'égalité doit entraîner le rejet.")

    def test_B5_majorite_des_exprimes_et_non_du_total(self):
        resultat = partie.depouiller(construire_votes(3, 1))
        self.assertTrue(resultat["adoptee"],
                        "B5 : 3 oui contre 1 non = 75 % des votes exprimés. "
                        "Les 6 absents ne comptent pas dans la majorité : "
                        "la proposition doit être adoptée.")


if __name__ == "__main__":
    unittest.main()
