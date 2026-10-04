# DAO Simulator

Un laboratoire open source pour tester, partie après partie, quelles règles permettraient à une DAO de gouverner une ville comme Metz, construit pour apprendre le métier de PO avec des agents.

## Objectifs

1. **Apprendre à développer avec Claude Code**, progressivement, jusqu'aux usages avancés.
2. **Comprendre comment fonctionne une DAO** en en construisant une, puis en observant ce qui la fait réussir ou échouer.
3. **Devenir un PO qui sait travailler avec des agents**, et documenter la méthode au fil de l'eau.

## État actuel

Version **V1** en cours : une partie complète se joue dans le terminal. Dix membres (4 prudents, 3 dépensiers, 3 absentéistes) votent tour après tour pour construire des bâtiments avec la trésorerie commune. La partie s'arrête sur une victoire (2 000 crédits), une défaite (trésorerie négative) ou au bout de 30 tours.

## Lancer une partie

Prérequis : Python 3 (aucune bibliothèque à installer).

```bash
python3 src/jouer.py
```

Chaque tour s'affiche sur une ligne, puis le résultat final. Les réglages (tokens, trésorerie, quorum, bâtiments, graine aléatoire…) se trouvent dans `src/reglages.py`. Avec la même graine, on obtient exactement la même partie.

## Lancer les tests

Des tests automatiques vérifient que le code respecte les règles de la spec V1 : quorum, majorité, profils de vote, construction, revenus, fin de partie, reproductibilité et réglages par défaut. Depuis la racine du projet :

```bash
python3 -m unittest discover -s tests -v
```

Chaque test affiche `ok` s'il passe. S'il échoue, un message explique la règle de la spec qui n'est pas respectée.

## Organisation

- `src/` : le code du simulateur. La commande `python3 src/jouer.py` lance une partie.
- `tests/` : les tests automatiques des règles du jeu.
- `docs/` : la documentation du projet, à commencer par le document de cadrage.
- `lecons/` : les leçons écrites au fil du projet, pour apprendre en partant de zéro.

## Feuille de route

Ce qui suit est un plan, pas encore une réalité :

- **V1–V2** : une DAO abstraite qui joue des parties complètes, avec rapports et comparaison de règles.
- **V3–V5** : une petite ville fictive, avec quartiers, budget et événements.
- **V6 et au-delà** : une Metz simplifiée, puis des habitants pilotés par une IA.

Le détail se trouve dans [`docs/cadrage.md`](docs/cadrage.md) (§13).

## Licences

- **Code** : licence MIT, voir le fichier [`LICENSE`](LICENSE).
- **Textes** (documentation et leçons) : [Creative Commons BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.fr).
