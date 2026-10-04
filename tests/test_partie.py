# Tests d'une partie complète : reproductibilité et cohérence du journal.
# Chaque valeur attendue est calculée à partir des règles de la spec, pas du code.
# Commande : python3 -m unittest discover -s tests -v

import os
import random
import sys
import unittest

# On indique à Python où trouver le code du simulateur (le dossier src/).
DOSSIER_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.insert(0, DOSSIER_SRC)

import partie


# Graine de la spec, tableau « Départ ».
GRAINE_ALEATOIRE = 42

# Valeurs de la spec, tableau « Départ ».
TRESORERIE_DE_DEPART = 500
FRAIS_FIXES = 30
NOMBRE_DE_TOURS_MAX = 30
OBJECTIF_DE_VICTOIRE = 2000


def jouer_avec_graine(graine):
    """Fixe la graine puis joue une partie complète."""
    random.seed(graine)
    return partie.jouer_partie()


class TestPartieComplete(unittest.TestCase):
    """Règles : la même graine produit exactement la même partie ; une partie suit les règles."""

    def test_G1_meme_graine_meme_partie(self):
        premiere = jouer_avec_graine(GRAINE_ALEATOIRE)
        seconde = jouer_avec_graine(GRAINE_ALEATOIRE)
        self.assertEqual(premiere, seconde,
                         "G1 : deux parties avec la graine 42 doivent être exactement identiques "
                         "(journal, issue, cause, nombre de tours).")

    def test_G2_fin_de_partie_coherente(self):
        donnees = jouer_avec_graine(GRAINE_ALEATOIRE)
        self.assertLessEqual(donnees["tours_joues"], NOMBRE_DE_TOURS_MAX,
                             "G2 : une partie dure au plus 30 tours.")
        self.assertEqual(len(donnees["journal"]), donnees["tours_joues"],
                         "G2 : le journal doit contenir une fiche par tour joué.")
        if donnees["issue"] == partie.ISSUE_VICTOIRE:
            self.assertGreaterEqual(donnees["tresorerie_finale"], OBJECTIF_DE_VICTOIRE,
                                    "G2 : une victoire exige une trésorerie finale d'au moins 2000.")
        else:
            perdue_par_tresorerie = donnees["tresorerie_finale"] < 0
            perdue_au_dernier_tour = donnees["tours_joues"] == NOMBRE_DE_TOURS_MAX
            self.assertTrue(perdue_par_tresorerie or perdue_au_dernier_tour,
                            "G2 : une défaite exige une trésorerie négative "
                            "ou le tour 30 atteint.")

    def test_G3_tresorerie_coherente_tour_apres_tour(self):
        donnees = jouer_avec_graine(GRAINE_ALEATOIRE)
        tresorerie_precedente = TRESORERIE_DE_DEPART
        for fiche in donnees["journal"]:
            # Le coût n'est payé que si le bâtiment est construit.
            cout_paye = 0
            if fiche["resultat"] == partie.RESULTAT_CONSTRUITE:
                cout_paye = fiche["proposition"]["cout"]
            attendue = tresorerie_precedente - cout_paye + fiche["revenus"] - FRAIS_FIXES
            self.assertEqual(fiche["tresorerie_fin_de_tour"], attendue,
                             "G3 : tour " + str(fiche["tour"]) + " : trésorerie précédente ("
                             + str(tresorerie_precedente) + ") − coût payé (" + str(cout_paye)
                             + ") + revenus (" + str(fiche["revenus"]) + ") − frais (30) = "
                             + str(attendue) + " attendu.")
            tresorerie_precedente = fiche["tresorerie_fin_de_tour"]


if __name__ == "__main__":
    unittest.main()
