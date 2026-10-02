# DAO Simulator

Un laboratoire open source pour tester, partie après partie, quelles règles permettraient à une DAO de gouverner une ville comme Metz, construit pour apprendre le métier de PO avec des agents.

## Objectifs

1. **Apprendre à développer avec Claude Code**, progressivement, jusqu'aux usages avancés.
2. **Comprendre comment fonctionne une DAO** en en construisant une, puis en observant ce qui la fait réussir ou échouer.
3. **Devenir un PO qui sait travailler avec des agents**, et documenter la méthode au fil de l'eau.

## État actuel

Version **V0** : un premier programme, `vote.py`, qui simule un seul vote de DAO. Dix membres votent au hasard (oui, non ou abstention), puis le programme vérifie le quorum et la majorité et affiche le résultat.

## Lancer le programme

Prérequis : Python 3 (aucune bibliothèque à installer).

```bash
python3 vote.py
```

Les réglages (nombre de membres, quorum, majorité, graine aléatoire) se trouvent en haut du fichier.

## Organisation

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
