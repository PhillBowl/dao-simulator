# CLAUDE.md

## Le projet

DAO Simulator est un laboratoire open source pour tester, partie après partie, quelles règles permettraient à une DAO de gouverner une ville comme Metz. Il avance par petites versions, une brique à la fois. Il sert aussi à apprendre le métier de PO avec des agents : la méthode compte autant que le simulateur.

Vision, règles du jeu et feuille de route : `docs/cadrage.md`.

## Qui je suis

- PO de métier, débutant complet en Python et en git.
- J'apprends en construisant ce projet avec toi.
- Mon objectif : devenir un PO capable de travailler avec des agents.

## Comment travailler avec moi

- Avant d'écrire du code, résume en quelques lignes ce que tu vas faire.
- Explique simplement. Définis chaque terme technique la première fois que tu l'emploies dans une session.
- À la fin d'une tâche, liste les choix que tu as faits sans que je les précise.
- Ne fais jamais de commit sans que je te le demande.
- Ne modifie que les fichiers concernés par la tâche. Si un autre fichier te semble à corriger, signale-le sans le toucher.

## Coaching de prompts

Avant une tâche importante (nouvelle fonctionnalité, modification de plusieurs fichiers), donne un retour court sur mon prompt :

1. ce qui marche ;
2. ce qui manque, parmi : contexte, objectif, contraintes, format de sortie, critère de fin ;
3. une structure proposée.

Ne réécris pas le prompt à ma place, sauf si je le demande.

## Conventions de code

- Python, bibliothèque standard uniquement, sauf décision explicite de ma part.
- Tout en français : commentaires, noms de variables et de fonctions, textes affichés.
- Les réglages sont des constantes en MAJUSCULES, regroupées en haut du fichier.
- Des petites fonctions, chacune avec un seul rôle, nommée par un verbe (`compter_tokens`, `afficher_resultat`).
- Un code lisible par un débutant plutôt que court ou astucieux : une étape par ligne, pas de lambda ni de compréhension de liste, un commentaire qui explique chaque bloc.
- Une graine aléatoire fixe (constante `GRAINE_ALEATOIRE`, passée à `random.seed()` au début du programme), pour des résultats reproductibles.
- Après une modification, lance le programme et vérifie qu'il s'exécute sans erreur.
- Avant de déclarer une tâche terminée, lance tous les tests : ils doivent tous passer. Ne modifie jamais un test pour le faire passer sans mon accord.

## Organisation des dossiers

- `docs/` : cadrage et specs de version.
- `lecons/` : les leçons, publiques.
- `journal/` : mon journal de bord, privé.
- `src/` : le code du simulateur.
- `tests/` : les tests automatiques, un fichier `test_*.py` par groupe de règles.
- Plus tard : `config/` (paramètres).

## Sécurité

- Aucun secret dans le dépôt : clé d'API, mot de passe, jeton d'accès.
- Ne lis et ne modifie jamais le contenu du dossier `journal/`.

## Commandes

- Lancer une partie : `python3 src/jouer.py`
- Lancer tous les tests : `python3 -m unittest discover -s tests -v`
