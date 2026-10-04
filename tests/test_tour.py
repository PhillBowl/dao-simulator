# Tests des étapes 4 à 7 d'un tour : exécution, revenus, frais, vérification de fin.
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


# Graine fixe : les tests du Marché donnent toujours le même résultat.
GRAINE_ALEATOIRE = 42

# Nombre de tours observés pour mesurer le revenu d'un Marché.
NOMBRE_DE_TIRAGES_MARCHE = 1000
NOMBRE_DE_TOURS_DEUX_MARCHES = 200

# « Pile ou face » entre 0 et 80 : environ 50 % de 80, fourchette large.
POURCENT_80_MINIMUM = 45
POURCENT_80_MAXIMUM = 55

# Coûts des bâtiments, tableau « Bâtiments » de la spec.
COUTS = {"Ferme": 100, "Atelier": 200, "Marché": 150}


def construire_proposition(batiment):
    """Fabrique une proposition pour le bâtiment voulu."""
    return {
        "auteur": "Membre 1",
        "profil_auteur": "dépensier",
        "batiment": batiment,
        "cout": COUTS[batiment],
    }


def construire_depouillement(adoptee):
    """Fabrique un dépouillement : les 10 membres votent tous oui, ou tous non."""
    if adoptee:
        choix = membres.OUI
    else:
        choix = membres.NON
    votes = []
    for numero in range(1, 11):
        votes.append({"nom": "Membre " + str(numero), "profil": "dépensier",
                      "tokens": 100, "vote": choix})
    return partie.depouiller(votes)


def construire_etat(tour, tresorerie):
    """Fabrique un état de la DAO au tour et avec la trésorerie voulus."""
    etat_dao = partie.creer_etat_dao()
    etat_dao["tour"] = tour
    etat_dao["tresorerie"] = tresorerie
    return etat_dao


def construire_batiment(etat_dao, batiment):
    """Fait adopter et construire un bâtiment au tour en cours de l'état."""
    return partie.executer(construire_proposition(batiment),
                           construire_depouillement(True), etat_dao)


def mesurer_revenu(etat_dao):
    """Encaisse les revenus du tour et renvoie de combien la trésorerie a augmenté."""
    avant = etat_dao["tresorerie"]
    partie.encaisser_revenus(etat_dao)
    return etat_dao["tresorerie"] - avant


def construire_etat_suivant(etat_dao):
    """Fait passer l'état au tour suivant (sans rien faire d'autre)."""
    etat_dao["tour"] = etat_dao["tour"] + 1
    return etat_dao


class TestExecution(unittest.TestCase):
    """Règle : construit si adoptée ET trésorerie supérieure ou égale au coût,
    sans tenir compte des frais fixes du tour."""

    def test_D1_adoptee_sans_fonds_suffisants(self):
        etat_dao = construire_etat(1, 150)
        resultat = construire_batiment(etat_dao, "Atelier")
        self.assertEqual(resultat, partie.RESULTAT_FONDS_INSUFFISANTS,
                         "D1 : Atelier à 200 adopté avec 150 en caisse : "
                         "adoptée mais non construite.")
        self.assertEqual(etat_dao["tresorerie"], 150,
                         "D1 : rien n'est construit, la trésorerie doit rester à 150.")
        self.assertEqual(mesurer_revenu(construire_etat_suivant(etat_dao)), 0,
                         "D1 : aucun bâtiment ne doit avoir été ajouté (aucun revenu au tour suivant).")

    def test_D2_tresorerie_egale_au_cout(self):
        etat_dao = construire_etat(1, 200)
        resultat = construire_batiment(etat_dao, "Atelier")
        self.assertEqual(resultat, partie.RESULTAT_CONSTRUITE,
                         "D2 : 200 en caisse pour un Atelier à 200 : « supérieure ou égale », "
                         "il doit être construit.")
        self.assertEqual(etat_dao["tresorerie"], 0,
                         "D2 : 200 − 200 = 0 attendu après paiement.")

    def test_D3_frais_fixes_ignores_pour_construire(self):
        etat_dao = construire_etat(1, 110)
        resultat = construire_batiment(etat_dao, "Ferme")
        self.assertEqual(resultat, partie.RESULTAT_CONSTRUITE,
                         "D3 : 110 en caisse pour une Ferme à 100 : construite, "
                         "sans tenir compte des 30 de frais du tour.")
        self.assertEqual(etat_dao["tresorerie"], 10,
                         "D3 : 110 − 100 = 10 attendu après paiement.")

    def test_D4_rejetee_rien_ne_change(self):
        etat_dao = construire_etat(1, 500)
        partie.executer(construire_proposition("Ferme"),
                        construire_depouillement(False), etat_dao)
        self.assertEqual(etat_dao["tresorerie"], 500,
                         "D4 : proposition rejetée : rien n'est payé, la trésorerie reste à 500.")
        self.assertEqual(mesurer_revenu(construire_etat_suivant(etat_dao)), 0,
                         "D4 : proposition rejetée : aucun bâtiment ne doit avoir été construit.")


class TestRevenusEtFrais(unittest.TestCase):
    """Règles : un bâtiment construit lors d'un tour précédent rapporte son revenu ;
    Ferme 20, Atelier 45, Marché 0 ou 80 à pile ou face, pour chaque marché ; frais 30."""

    def test_E1_construit_ce_tour_ci_ne_rapporte_rien(self):
        etat_dao = construire_etat(5, 500)
        construire_batiment(etat_dao, "Ferme")
        self.assertEqual(mesurer_revenu(etat_dao), 0,
                         "E1 : Ferme construite au tour 5 : elle ne rapporte rien au tour 5.")

    def test_E2_construits_au_tour_precedent_rapportent(self):
        etat_dao = construire_etat(5, 500)
        construire_batiment(etat_dao, "Ferme")
        construire_batiment(etat_dao, "Atelier")
        construire_etat_suivant(etat_dao)
        self.assertEqual(mesurer_revenu(etat_dao), 65,
                         "E2 : Ferme et Atelier construits au tour 5 : "
                         "au tour 6 ils rapportent 20 + 45 = 65.")

    def test_E3_enchainement_de_deux_tours(self):
        # Tour 1 : 500 − 100 (Ferme) + 0 (pas encore de revenu) − 30 (frais) = 370.
        etat_dao = construire_etat(1, 500)
        construire_batiment(etat_dao, "Ferme")
        partie.encaisser_revenus(etat_dao)
        partie.payer_frais(etat_dao)
        self.assertEqual(etat_dao["tresorerie"], 370,
                         "E3 : tour 1 : 500 − 100 + 0 − 30 = 370 attendu.")
        # Tour 2 : rien d'adopté ; 370 + 20 (Ferme) − 30 (frais) = 360.
        construire_etat_suivant(etat_dao)
        partie.encaisser_revenus(etat_dao)
        partie.payer_frais(etat_dao)
        self.assertEqual(etat_dao["tresorerie"], 360,
                         "E3 : tour 2 : 370 + 20 − 30 = 360 attendu.")

    def test_E4_frais_fixes(self):
        etat_dao = construire_etat(1, 500)
        partie.payer_frais(etat_dao)
        self.assertEqual(etat_dao["tresorerie"], 470,
                         "E4 : frais fixes de 30 : 500 − 30 = 470 attendu.")

    def test_E5_revenu_du_marche(self):
        random.seed(GRAINE_ALEATOIRE)
        etat_dao = construire_etat(1, 500)
        construire_batiment(etat_dao, "Marché")
        revenus = []
        for _ in range(NOMBRE_DE_TIRAGES_MARCHE):
            construire_etat_suivant(etat_dao)
            revenus.append(mesurer_revenu(etat_dao))
        # Chaque revenu vaut 0 ou 80.
        for revenu in revenus:
            self.assertIn(revenu, [0, 80],
                          "E5 : un Marché rapporte 0 ou 80, obtenu " + str(revenu) + ".")
        # Pile ou face : environ la moitié des tours à 80.
        pourcent_80 = revenus.count(80) * 100 / NOMBRE_DE_TIRAGES_MARCHE
        self.assertTrue(POURCENT_80_MINIMUM <= pourcent_80 <= POURCENT_80_MAXIMUM,
                        "E5 : « pile ou face » donne environ 50 % de tours à 80 "
                        "(attendu entre " + str(POURCENT_80_MINIMUM) + " et "
                        + str(POURCENT_80_MAXIMUM) + " %), obtenu "
                        + str(round(pourcent_80, 1)) + " %.")

    def test_E6_un_tirage_pour_chaque_marche(self):
        random.seed(GRAINE_ALEATOIRE)
        etat_dao = construire_etat(1, 500)
        construire_batiment(etat_dao, "Marché")
        construire_batiment(etat_dao, "Marché")
        revenus = []
        for _ in range(NOMBRE_DE_TOURS_DEUX_MARCHES):
            construire_etat_suivant(etat_dao)
            revenus.append(mesurer_revenu(etat_dao))
        # Un total de 80 signifie qu'un marché a rapporté 80 et l'autre 0.
        self.assertIn(80, revenus,
                      "E6 : avec deux marchés tirés séparément, au moins un tour doit "
                      "donner 80 + 0 = 80. Seuls 0 et 160 signifieraient un tirage commun.")


class TestFinDePartie(unittest.TestCase):
    """Règles : sur la trésorerie de fin de tour, victoire si elle atteint 2000 ;
    défaite si elle est négative ; défaite si le tour 30 est atteint sans victoire."""

    def verifier(self, tour, tresorerie):
        """Demande si la partie est finie au tour et avec la trésorerie donnés."""
        return partie.verifier_fin(construire_etat(tour, tresorerie))

    def test_F1_victoire(self):
        fin = self.verifier(10, 2000)
        self.assertIsNotNone(fin, "F1 : 2000 au tour 10 : la partie doit s'arrêter.")
        self.assertEqual(fin["issue"], partie.ISSUE_VICTOIRE,
                         "F1 : 2000 atteint l'objectif : victoire attendue.")

    def test_F2_juste_sous_l_objectif(self):
        self.assertIsNone(self.verifier(10, 1999),
                          "F2 : 1999 au tour 10 : ni victoire ni défaite, la partie continue.")

    def test_F3_tresorerie_a_zero(self):
        self.assertIsNone(self.verifier(10, 0),
                          "F3 : 0 au tour 10 : « une trésorerie à exactement 0 n'est pas "
                          "une défaite », la partie continue.")

    def test_F4_tresorerie_negative(self):
        fin = self.verifier(10, -1)
        self.assertIsNotNone(fin, "F4 : −1 au tour 10 : la partie doit s'arrêter.")
        self.assertEqual(fin["issue"], partie.ISSUE_DEFAITE,
                         "F4 : trésorerie négative : défaite attendue.")

    def test_F5_victoire_au_tour_30(self):
        fin = self.verifier(30, 2000)
        self.assertIsNotNone(fin, "F5 : 2000 au tour 30 : la partie doit s'arrêter.")
        self.assertEqual(fin["issue"], partie.ISSUE_VICTOIRE,
                         "F5 : « la victoire compte si l'objectif est atteint à la fin "
                         "du tour 30 » : victoire attendue.")

    def test_F6_dernier_tour_sans_victoire(self):
        fin = self.verifier(30, 1999)
        self.assertIsNotNone(fin, "F6 : tour 30 atteint : la partie doit s'arrêter.")
        self.assertEqual(fin["issue"], partie.ISSUE_DEFAITE,
                         "F6 : 1999 au tour 30 : défaite attendue (dernier tour sans victoire).")

    def test_F7_negative_au_dernier_tour(self):
        fin = self.verifier(30, -10)
        reference_negative = self.verifier(10, -1)
        self.assertEqual(fin["issue"], partie.ISSUE_DEFAITE,
                         "F7 : −10 au tour 30 : défaite attendue.")
        self.assertEqual(fin["cause"], reference_negative["cause"],
                         "F7 : « une trésorerie négative au dernier tour est une défaite pour "
                         "trésorerie négative » : même cause attendue qu'en F4.")

    def test_F8_zero_au_dernier_tour(self):
        fin = self.verifier(30, 0)
        reference_dernier_tour = self.verifier(30, 1999)
        self.assertEqual(fin["issue"], partie.ISSUE_DEFAITE,
                         "F8 : 0 au tour 30 : défaite attendue (dernier tour sans victoire).")
        self.assertEqual(fin["cause"], reference_dernier_tour["cause"],
                         "F8 : 0 n'est pas une trésorerie négative : la cause doit être "
                         "« dernier tour atteint », comme en F6.")


if __name__ == "__main__":
    unittest.main()
