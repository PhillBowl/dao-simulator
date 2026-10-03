# Leçon 2 — De la spec au plan

> Version V1 · US1 · Durée estimée : deux sessions de 2 heures

---

## 1. Ce qu'on va faire

Poser la **spec de la V1** et son **backlog**, puis faire construire la première user story (US1 : jouer une partie complète) en passant par le **mode plan** : Claude propose un plan de travail, je le relis et je le valide avant qu'il ne touche au moindre fichier.

---

## 2. Le concept

### Du cadrage à la spec

| Document | Question à laquelle il répond | Horizon |
|---|---|---|
| Cadrage | Pourquoi ce projet, et où va-t-il ? | Tout le projet |
| Spec de version | Que doit faire précisément cette version ? | Une version |
| Backlog | Dans quel ordre, et où en est-on ? | Une version |
| `CLAUDE.md` | Comment l'agent doit-il travailler ? | Chaque session |

La spec est écrite au format de mes tickets habituels : contexte, user story, objectif, inclus, critères d'acceptation. Les **critères d'acceptation** sont le cœur : ce sont eux que je vérifierai un par un à la fin. S'ils sont flous, je ne pourrai pas dire si c'est terminé.

### Le travail principal d'une spec : trancher les zones floues

Le cadrage disait « le Marché rapporte 0 ou 80 au hasard ». Une fois par partie ? À chaque tour ? Pour chaque marché ? Un agent qui rencontre ce flou choisit une réponse, souvent sans le dire. La spec de la V1 tranche cinq zones floues de ce genre (rubrique « Zones floues du cadrage tranchées par cette spec »). **Une règle métier laissée floue est une règle métier décidée par l'agent.**

### Le mode plan

En mode plan, Claude **lit les fichiers et propose un plan, mais ne modifie rien** tant que je ne l'ai pas approuvé. C'est l'équivalent d'une séance d'affinage avec un développeur : il explique comment il compte s'y prendre, je pose des questions, je corrige, puis je valide.

Pourquoi c'est précieux :
- je repère un malentendu **avant** qu'il ne devienne du code ;
- je vérifie que le périmètre est respecté (US1, et rien d'autre) ;
- je comprends l'architecture proposée, ce qui m'aidera à relire le code ensuite.

---

## 3. Pourquoi maintenant

La V1 est la première vraie construction : plusieurs fichiers, une architecture, des règles nombreuses. Sans spec ni plan, Claude produirait quelque chose d'impressionnant, mais je ne saurais ni vérifier si c'est juste, ni comprendre comment c'est organisé.

---

## 4. L'outil Claude Code : le mode plan

- **Entrer en mode plan** : appuyer sur `Maj + Tab` (la touche Shift et la touche Tab), plusieurs fois si besoin, jusqu'à voir `⏸ plan mode on` en bas de l'écran.
- **Pendant le mode plan** : Claude lit, explore, pose des questions, et rédige un plan. Il ne crée, ne modifie et ne supprime aucun fichier.
- **À la fin**, Claude présente son plan et demande s'il peut l'exécuter. Je peux :
  - l'approuver : Claude sort du mode plan et commence à travailler ;
  - refuser et demander des modifications : le plan est retravaillé.
- **Référencer un fichier** dans un prompt : taper `@` suivi du chemin, par exemple `@docs/specs/spec-v1.md`. Le fichier est joint au message.

---

## 5. L'exercice, pas à pas

### Étape 1 — Lire et ranger la spec et le backlog

Télécharger `spec-v1.md` et `backlog.md` depuis la conversation, puis, une commande à la fois :

```bash
cd ~/dao-simulator
```

```bash
mkdir docs/specs
```

```bash
mv ~/Downloads/spec-v1.md docs/specs/spec-v1.md
```

```bash
mv ~/Downloads/backlog.md docs/backlog.md
```

Puis **lire la spec en entier** dans VS Code :

```bash
code docs/specs/spec-v1.md
```

C'est ma spec : je la signe. Pour chaque règle, je me demande si je suis d'accord. Si non, je la modifie maintenant. Attention en particulier aux « zones floues tranchées » : ce sont des décisions de gouvernance du jeu.

### Étape 2 — Committer la spec avant le code

```bash
git add docs
```

```bash
git commit -m "Spec et backlog de la V1"
```

La spec entre dans l'historique **avant** le code. Plus tard, on pourra toujours vérifier ce qui était demandé, indépendamment de ce qui a été livré.

### Étape 3 — Lancer Claude en mode plan

```bash
claude
```

Puis `Maj + Tab` jusqu'à voir `⏸ plan mode on`.

### Étape 4 — Le prompt de planification

Coller ce modèle (les commentaires qui suivent expliquent chaque partie) :

```
Lis @CLAUDE.md et @docs/specs/spec-v1.md.

Je veux réaliser l'US1 « Jouer une partie complète », et uniquement l'US1 : pas de tests, pas de fichier de configuration, pas de rapport HTML. Ce sont les US suivantes.

Propose-moi un plan qui précise :
1. Les fichiers que tu vas créer, modifier ou supprimer, avec le rôle de chacun en une phrase.
2. Comment la partie (le modèle) et les membres sont séparés, et comment les trois profils répondent à la même question « voici la proposition et l'état de la DAO, que votes-tu ? ».
3. La commande qui lancera une partie.
4. L'ordre des étapes de réalisation.
5. Comment tu vérifieras chacun des critères d'acceptation de l'US1.
6. Les points de la spec qui te paraissent ambigus ou contradictoires. Ne les tranche pas seul : pose-moi la question.

Explique le plan simplement : je dois pouvoir le comprendre sans connaître Python.
```

**Pourquoi ce prompt est construit ainsi**
- **« Uniquement l'US1 »**, avec la liste de ce qui est exclu : un agent motivé a tendance à en faire plus que demandé. On borne le périmètre explicitement.
- **Les points 1 à 4** donnent la forme du plan : je saurai quoi relire.
- **Le point 5** relie le plan aux critères d'acceptation : la recette est préparée dès la conception.
- **Le point 6** est le plus important : il oblige Claude à faire remonter les zones floues au lieu de les trancher en silence.
- **« Sans connaître Python »** : le plan est un document pour le PO, pas pour un développeur.

### Étape 5 — Relire le plan

Avant d'approuver, six questions :

1. **Périmètre** : le plan se limite-t-il à l'US1 ? Rien sur les tests, la configuration, le rapport ?
2. **Fichiers** : est-ce que je comprends le rôle de chaque fichier ? Le code est-il bien dans `src/`, et `vote.py` supprimé ?
3. **Séparation** : la partie et les membres sont-ils dans des endroits distincts ?
4. **Règles** : le plan reprend-il les règles de la spec, sans en inventer ?
5. **Critères** : chaque critère d'acceptation a-t-il sa vérification ?
6. **Questions** : Claude a-t-il signalé des ambiguïtés ? Si oui, je réponds, et je **reporte la réponse dans la spec** pour qu'elle reste la référence.

Si une réponse est non, je le dis à Claude et je lui demande de corriger le plan. On peut faire plusieurs allers-retours : c'est le moment le moins coûteux pour changer d'avis.

Quand tout est bon : j'approuve.

### Étape 6 — L'exécution

Claude sort du mode plan et travaille. Je lis chaque demande de permission. La suppression de `vote.py` est attendue ; toute autre suppression doit m'interroger.

### Étape 7 — La recette

Je vérifie moi-même chaque critère d'acceptation de l'US1, en cochant ce tableau dans mon journal :

| Critère | Comment je le vérifie | OK ? |
|---|---|---|
| Une seule commande lance une partie, documentée | Je lance la commande ; je la retrouve dans le README et `CLAUDE.md` | |
| Une ligne par tour, avec toutes les informations | Je lis la sortie | |
| Résultat, cause et nombre de tours affichés | Je lis la fin de la sortie | |
| Même graine, même partie | Je lance deux fois, je compare | |
| Règles conformes à la spec | Je prends un tour au hasard et je refais le calcul à la main : participation, quorum, majorité, trésorerie | |
| Code dans `src/`, partie et membres séparés | J'ouvre les fichiers dans VS Code | |
| `vote.py` supprimé | `ls` | |

Le contrôle d'un tour à la main est essentiel : c'est la seule façon de savoir si les règles sont bien appliquées, tant qu'il n'y a pas de tests (US2).

Ensuite, je lis la liste des **choix non demandés** de Claude, et je décide pour chacun : j'accepte, ou je demande une modification.

### Étape 8 — Mettre à jour le backlog

Dans `docs/backlog.md`, passer l'US1 à « Terminé ».

### Étape 9 — Commit et envoi sur GitHub

```bash
git status
```

La liste doit contenir les nouveaux fichiers de `src/`, la suppression de `vote.py`, le README, le `CLAUDE.md` et le backlog modifiés. Rien d'inattendu ? Alors :

```bash
git add .
```

Le point signifie « tout ce qui a changé dans le dossier ». C'est pratique, mais je ne l'utilise **qu'après avoir lu `git status`** : le `.gitignore` protège le journal et les secrets, mais pas un fichier inattendu.

```bash
git commit -m "US1 : jouer une partie complète"
```

```bash
git push
```

`git push` envoie les nouveaux commits sur GitHub. Le dépôt en ligne est à jour.

### Étape 10 — Journal

Les points à noter cette fois : les questions que Claude a soulevées en mode plan, les corrections que j'ai demandées au plan, et le résultat de la recette.

---

## 6. Ce que ça change pour un PO

- **La spec est un contrat, les critères d'acceptation sont la recette.** Ils sont écrits avant le code, et vérifiés après.
- **Le mode plan est un affinage.** Le PO y valide la compréhension du besoin et le périmètre, pas le détail technique.
- **Les zones floues sont le vrai travail du PO.** Un développeur humain pose des questions quand il doute ; un agent, souvent, tranche. Il faut lui demander explicitement de remonter les ambiguïtés.
- **Une réponse donnée en séance doit revenir dans la spec**, sinon elle sera perdue à la session suivante.
- **Une US à la fois.** Petits incréments, chacun recetté, chacun committé.

---

## 7. Les pièges

- **Approuver un plan sans le lire** : c'est valider un développement sans l'avoir compris.
- **Un plan qui déborde** : des tests, une configuration, un rapport « tant qu'on y est ». On refuse, on recentre.
- **Laisser une ambiguïté se trancher en silence** : vérifier la liste des questions et des choix non demandés.
- **Sortir du mode plan par erreur** avec `Maj + Tab` : vérifier l'indication en bas de l'écran avant d'envoyer le prompt.
- **Faire `git add .` sans lire `git status`.**
- **Une session trop longue** : si Claude semble perdre le fil, on termine l'étape en cours, on quitte, et on relance une session neuve. Le `CLAUDE.md` et la spec lui redonnent le contexte.

---

## Checklist de fin de leçon

- [ ] la spec et le backlog sont relus, ajustés et committés avant le code
- [ ] le plan a été relu avec les six questions, et corrigé si besoin
- [ ] les réponses aux ambiguïtés sont reportées dans la spec
- [ ] chaque critère d'acceptation de l'US1 est vérifié, dont un tour recalculé à la main
- [ ] les choix non demandés sont passés en revue
- [ ] le backlog est à jour, le commit est envoyé sur GitHub
- [ ] l'entrée de journal est écrite

**Prochaine leçon** : US2, les tests automatiques. Je découvrirai comment faire écrire des tests **avant** le code qu'ils vérifient, et pourquoi c'est la meilleure protection contre un agent trop sûr de lui.
