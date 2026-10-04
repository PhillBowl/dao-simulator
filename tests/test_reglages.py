# Tests des réglages par défaut : ils doivent correspondre exactement à la spec V1
# (tableaux « Départ », « Bâtiments » et « Profils »).
# Chaque valeur attendue est recopiée de la spec, pas du code.
# Commande : python3 -m unittest discover -s tests -v

import os
import sys
import unittest

# On indique à Python où trouver le code du simulateur (le dossier src/).
DOSSIER_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.insert(0, DOSSIER_SRC)

import reglages


class TestReglagesDepart(unittest.TestCase):
    """Tableau « Départ » de la spec."""

    def test_H1_membres_et_tokens(self):
        nombre_de_membres = 0
        for profil in reglages.REPARTITION_DES_PROFILS:
            nombre_de_membres = nombre_de_membres + reglages.REPARTITION_DES_PROFILS[profil]
        self.assertEqual(nombre_de_membres, 10, "H1 : la spec prévoit 10 membres.")
        self.assertEqual(reglages.TOKENS_PAR_MEMBRE, 100,
                         "H1 : la spec prévoit 100 tokens par membre.")

    def test_H2_tresorerie_frais_tours_objectif(self):
        self.assertEqual(reglages.TRESORERIE_DE_DEPART, 500,
                         "H2 : la spec prévoit une trésorerie de départ de 500 crédits.")
        self.assertEqual(reglages.FRAIS_FIXES, 30,
                         "H2 : la spec prévoit des frais fixes de 30 crédits par tour.")
        self.assertEqual(reglages.NOMBRE_DE_TOURS_MAX, 30,
                         "H2 : la spec prévoit 30 tours au maximum.")
        self.assertEqual(reglages.OBJECTIF_DE_VICTOIRE, 2000,
                         "H2 : la spec prévoit un objectif de victoire de 2000 crédits.")

    def test_H3_quorum_majorite_graine(self):
        self.assertEqual(reglages.QUORUM_POURCENT, 40,
                         "H3 : la spec prévoit un quorum de 40 % des tokens.")
        self.assertEqual(reglages.MAJORITE_POURCENT, 50,
                         "H3 : la spec prévoit une majorité de strictement plus de 50 %.")
        self.assertEqual(reglages.GRAINE_ALEATOIRE, 42,
                         "H3 : la spec prévoit la graine aléatoire 42.")


class TestReglagesBatiments(unittest.TestCase):
    """Tableau « Bâtiments » de la spec."""

    def test_H4_liste_des_batiments(self):
        noms = []
        for nom in reglages.BATIMENTS:
            noms.append(nom)
        self.assertCountEqual(noms, ["Ferme", "Atelier", "Marché"],
                              "H4 : la spec prévoit trois bâtiments : Ferme, Atelier, Marché.")

    def test_H5_couts_et_revenus(self):
        # Pour chaque bâtiment de la spec : son coût et ses revenus possibles.
        attendus = {
            "Ferme": (100, [20]),
            "Atelier": (200, [45]),
            "Marché": (150, [0, 80]),
        }
        for nom in attendus:
            cout_attendu = attendus[nom][0]
            revenus_attendus = attendus[nom][1]
            self.assertEqual(reglages.BATIMENTS[nom]["cout"], cout_attendu,
                             "H5 : la spec prévoit un coût de " + str(cout_attendu)
                             + " pour " + nom + ".")
            self.assertCountEqual(reglages.BATIMENTS[nom]["revenus_possibles"], revenus_attendus,
                                  "H5 : la spec prévoit les revenus " + str(revenus_attendus)
                                  + " pour " + nom + ".")


class TestReglagesProfils(unittest.TestCase):
    """Tableau « Profils » de la spec."""

    def test_H6_repartition_4_3_3(self):
        self.assertEqual(reglages.REPARTITION_DES_PROFILS,
                         {"prudent": 4, "dépensier": 3, "absentéiste": 3},
                         "H6 : la spec prévoit 4 prudents, 3 dépensiers, 3 absentéistes.")

    def test_H7_seuils_des_profils(self):
        self.assertEqual(reglages.SEUIL_PRUDENT_POURCENT, 30,
                         "H7 : un prudent accepte un coût jusqu'à 30 % de la trésorerie.")
        self.assertEqual(reglages.CHANCE_DE_VOTER_ABSENTEISTE, 3,
                         "H7 : un absentéiste vote avec une chance sur trois.")


if __name__ == "__main__":
    unittest.main()
