# Spec V1 — La Minimum Viable DAO

> Statut : validée · Version 1.0 · 03/10/2026
> Référence : `docs/cadrage.md`, §11 (règles de la V1) et §18 (critère de réussite)

---

## Contexte

La V0 simule un seul vote (`vote.py`). La V1 transforme ce prototype en une vraie partie : une DAO de 10 membres, une trésorerie, des bâtiments à construire, 30 tours, une victoire ou une défaite. C'est la première version jouable du simulateur, celle de l'étape A du cadrage (DAO abstraite).

## Question de recherche

Comment le quorum change-t-il le déroulement d'une partie ?

## Objectif

Pouvoir lancer une partie complète, la rejouer à l'identique, en modifier les réglages, et lire un rapport qui explique ce qui s'est passé.

## Inclus

- Une partie complète de 30 tours au maximum, jouée dans le terminal.
- Trois profils de membres à règles simples.
- Trois bâtiments.
- Les réglages dans un fichier, avec sauvegarde, chargement et réinitialisation.
- Des tests automatiques sur les règles de vote.
- Un rapport HTML : résumé, journal, graphiques, leçons.

## Exclu

Modes duel et série (V2), ville et quartiers (V3), événements (V3), délégation (V6), agents IA (V8), interface graphique de jeu. L'information reste parfaite : chaque membre connaît la trésorerie exacte.

---

## Règles du jeu

### Départ

| Élément | Valeur par défaut |
|---|---|
| Membres | 10, nommés « Membre 1 » à « Membre 10 » |
| Tokens par membre | 100 |
| Trésorerie de départ | 500 crédits |
| Frais fixes | 30 crédits par tour |
| Nombre de tours maximum | 30 |
| Objectif de victoire | 2 000 crédits |
| Quorum | 40 % des tokens |
| Majorité | strictement plus de 50 % des votes exprimés |
| Graine aléatoire | 42 |

### Bâtiments

| Bâtiment | Coût | Revenu par tour |
|---|---|---|
| Ferme | 100 | 20 |
| Atelier | 200 | 45 |
| Marché | 150 | 0 ou 80, tiré à pile ou face, à chaque tour et pour chaque marché |

### Profils

| Profil | Nombre | Comportement |
|---|---|---|
| Prudent | 4 | Oui si le coût est inférieur ou égal à 30 % de la trésorerie au moment du vote ; sinon non |
| Dépensier | 3 | Toujours oui |
| Absentéiste | 3 | Vote avec une chance sur trois ; s'il vote, oui ou non à pile ou face |

### Déroulement d'un tour

1. **Proposition** : un membre tiré au hasard (quel que soit son profil) propose un bâtiment tiré au hasard parmi les trois.
2. **Vote** : chaque membre vote oui, non, ou ne vote pas, selon son profil.
3. **Dépouillement** : quorum atteint si les tokens des votants (oui + non) représentent au moins le quorum du total ; si oui, adoption si les oui dépassent strictement la majorité des votes exprimés. Une égalité entraîne le rejet.
4. **Exécution** : si la proposition est adoptée **et** que la trésorerie couvre le coût, le bâtiment est construit et payé. Si la trésorerie est insuffisante, la proposition est adoptée mais non construite, et le journal le signale.
5. **Revenus** : chaque bâtiment construit **lors d'un tour précédent** rapporte son revenu. Un bâtiment construit ce tour-ci rapporte à partir du tour suivant.
6. **Frais** : on retire les frais fixes.
7. **Vérification**, sur la trésorerie de fin de tour : victoire si elle atteint l'objectif ; défaite si elle est négative ; défaite si le dernier tour est atteint sans victoire.

### Zones floues du cadrage tranchées par cette spec

Le cadrage laissait plusieurs points ouverts. Ils sont décidés ici :
- le revenu du Marché est tiré à chaque tour, pour chaque marché ;
- un absentéiste qui vote choisit oui ou non à pile ou face ;
- un bâtiment ne rapporte qu'à partir du tour suivant sa construction ;
- une proposition adoptée sans fonds suffisants n'est pas construite ;
- la vérification de victoire ou de défaite se fait en fin de tour.

---

## User stories

### US1 — Jouer une partie complète

**User story** : en tant que rédacteur de la constitution, je veux lancer une partie complète dans le terminal, afin de voir comment la DAO évolue tour après tour.

**Inclus** : le moteur de partie, les trois profils, les trois bâtiments, l'affichage tour par tour, le résultat final.

**Critères d'acceptation**
- Une seule commande lance une partie. Elle est documentée dans le README et dans `CLAUDE.md`.
- Chaque tour s'affiche sur une ligne : numéro, auteur et bâtiment proposé, votes (oui, non, participation), résultat, trésorerie de fin de tour.
- La partie s'arrête sur victoire, défaite ou dernier tour, et affiche le résultat, sa cause et le nombre de tours joués.
- La même graine produit exactement la même partie.
- Les règles appliquées sont celles de cette spec, réglages par défaut compris.
- Le code est rangé dans `src/`. La partie (le « modèle ») et les membres sont séparés. Tous les profils répondent à la même question : « voici la proposition et l'état de la DAO, que votes-tu ? ».
- `vote.py` est supprimé : sa logique est reprise dans `src/`.

### US2 — Tester les règles

**User story** : en tant que PO, je veux des tests automatiques sur les règles de vote, afin d'être sûr qu'une modification future ne casse pas ce qui marche.

**Inclus** : des tests avec `unittest` (fourni avec Python) dans `tests/`.

**Critères d'acceptation**
- Une seule commande lance tous les tests. Elle est documentée.
- Sont testés au minimum : le quorum (atteint, non atteint, exactement au seuil), la majorité (adoptée, rejetée, égalité), chaque profil de vote, l'adoption sans fonds suffisants, la reproductibilité avec une même graine.
- Tous les tests passent.
- Un test qui échoue affiche un message compréhensible.

### US3 — Régler, sauvegarder, réinitialiser

**User story** : en tant que rédacteur de la constitution, je veux modifier les réglages sans toucher au code, et pouvoir revenir aux valeurs par défaut, afin d'expérimenter librement.

**Inclus** : un fichier de réglages par défaut dans `config/`, des configurations nommées, et les commandes associées.

**Critères d'acceptation**
- Tous les réglages du tableau « Départ » et la répartition des profils sont dans `config/defaut.json`.
- Je peux lancer une partie avec une configuration nommée (par exemple `quorum-bas`).
- Je peux sauvegarder une configuration sous un nom, et la recharger.
- Une commande réinitialise : la partie suivante utilise les valeurs par défaut.
- Un réglage invalide (quorum de 150 %, nombre de tours négatif) produit un message d'erreur clair, pas un plantage.
- La configuration utilisée est affichée au début de chaque partie.

### US4 — Le rapport de partie

**User story** : en tant que rédacteur de la constitution, je veux un rapport visuel après chaque partie, afin de comprendre ce qui s'est passé sans relire tout le journal.

**Inclus** : une page HTML générée à la fin de chaque partie, dans un dossier `rapports/` exclu de git.

**Critères d'acceptation**
- Le rapport contient : un résumé (résultat, tours, cause), le journal tour par tour, et quatre graphiques : trésorerie au fil des tours, participation à chaque vote, propositions adoptées / rejetées / rejetées faute de quorum, poids de chaque profil dans les décisions adoptées.
- Le rapport rappelle la configuration utilisée.
- Le rapport s'ouvre dans un navigateur par double-clic.
- La simulation et le rapport sont séparés : la partie produit des données, le rapport les lit.

**Décision à prendre avant US4** : comment dessiner les graphiques.

| Option | Avantage | Inconvénient |
|---|---|---|
| Une bibliothèque de graphiques en JavaScript dans la page HTML | Simple, joli, interactif ; Python reste en bibliothèque standard | Le rapport a besoin d'Internet pour s'afficher |
| Dessiner les graphiques à la main en SVG depuis Python | Aucune dépendance, fonctionne hors ligne | Plus de code, rendu plus sobre |
| Installer une bibliothèque Python de graphiques (matplotlib) | Standard, très complet | Première dépendance à installer ; enfreint la règle « bibliothèque standard » |

### US5 — Les leçons automatiques

**User story** : en tant que rédacteur de la constitution, je veux que le rapport tire des leçons des chiffres, afin d'identifier rapidement ce qui a bloqué ou fait réussir la DAO.

**Inclus** : au moins trois règles de détection, affichées dans le rapport.

**Critères d'acceptation**
- Au moins trois leçons possibles, par exemple :
  - la part des propositions rejetées faute de quorum ;
  - le profil qui a le plus souvent bloqué les investissements ;
  - le nombre de tours écoulés avant la première construction, et les frais perdus pendant ce temps.
- Chaque leçon cite ses chiffres.
- Chaque leçon est formulée au conditionnel des hypothèses : elle décrit ce que produisent ces règles avec ces profils, pas une vérité sur les DAO.
- Une leçon sans objet (par exemple, aucune proposition rejetée faute de quorum) n'est pas affichée.

---

## Définition de terminé

La V1 est terminée quand les cinq user stories respectent leurs critères d'acceptation, et que le rituel de clôture est fait : rétrospective dans le journal, relecture du cadrage, article publié (cadrage, §15 et §18).
