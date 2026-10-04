# Leçon 3 — Des tests écrits depuis la spec

> Version V1 · US2 · Durée estimée : une à deux sessions de 2 heures

---

## 1. Ce qu'on va faire

Faire écrire par Claude des **tests automatiques** qui vérifient les règles du jeu, **à partir de la spec et non du code**. Puis casser volontairement une règle pour voir les tests la détecter, et la réparer avec git.

---

## 2. Le concept

### Un test, c'est une recette automatique

À la leçon 2, j'ai recalculé des tours à la main pour vérifier les règles. Un **test automatique** fait la même chose, mais en une seconde, à chaque modification, sans jamais se fatiguer :

```
Situation : trésorerie de 360, proposition à 100, membre prudent
Attendu   : il vote oui (100 / 360 = 28 %, sous le seuil de 30 %)
Constaté  : ce que le code répond
→ identiques : le test passe (OK) ; différents : il échoue (FAIL)
```

Un ensemble de tests s'appelle une **suite de tests**. Python fournit un outil pour les écrire et les lancer : `unittest`.

### À quoi ça sert vraiment : la non-régression

Une **régression**, c'est casser en modifiant B quelque chose qui marchait dans A. Plus le simulateur grandira, plus ce risque augmentera, surtout avec un agent qui peut modifier plusieurs fichiers en une fois. Les tests sont le filet de sécurité : ils tournent à chaque modification et signalent immédiatement ce qui a cassé.

### Pourquoi depuis la spec, et pas depuis le code

Si Claude écrit les tests en lisant son propre code, il risque de recopier ses erreurs : le test vérifiera que le code fait… ce que fait le code. Un test utile vérifie que le code fait **ce que la spec demande**.

D'où trois règles pour cette leçon :
1. **Chaque valeur attendue vient de la spec**, calculée à la main, jamais lue dans le code.
2. **Si un test échoue, on ne modifie pas le test pour qu'il passe.** On cherche qui a raison : la spec ou le code.
3. **Claude ne corrige pas le code de lui-même** : il signale l'écart, et c'est moi qui décide.

C'est la règle d'or avec un agent : **il ne note pas sa propre copie**.

---

## 3. Pourquoi maintenant

L'US1 a des règles nombreuses et des cas limites (égalité, seuil exact, trésorerie à zéro). L'US3 va bientôt toucher au code pour lire les réglages dans un fichier : c'est exactement le genre de modification qui provoque des régressions. Il faut le filet avant de commencer.

---

## 4. Les outils

- **`unittest`** : l'outil de test fourni avec Python. Rien à installer.
- **Le résultat d'une suite de tests** : une ligne de points (un point par test réussi, un `F` par échec), puis `OK` ou `FAILED`, avec le détail des échecs.
- **`git restore <fichier>`** : annule les modifications non commitées d'un fichier, et le remet dans l'état du dernier commit. C'est le bouton « revenir à la dernière photo ».

---

## 5. L'exercice, pas à pas

### Étape 1 — Planifier les tests en mode plan

```bash
cd ~/dao-simulator
```

```bash
claude
```

`Maj + Tab` jusqu'à `⏸ plan mode on`, puis ce prompt :

```
Lis @CLAUDE.md et @docs/specs/spec-v1.md.

Je veux réaliser l'US2 « Tester les règles », et uniquement l'US2 : pas de fichier de configuration, pas de rapport.

Règles impératives :
- Chaque valeur attendue d'un test vient de la spec, calculée à partir de ses règles. Ne la déduis jamais du code.
- Tu peux lire le code de src/ uniquement pour savoir quelles fonctions appeler.
- Si un test révèle un écart entre la spec et le code, ne modifie ni le test ni le code : signale-moi l'écart.
- Ne modifie aucun fichier de src/.

Propose-moi un plan qui contient :
1. Les fichiers de tests à créer, et la commande unique pour lancer tous les tests.
2. Un tableau des cas de test, avec pour chacun : la situation, la règle de la spec qui s'applique (citée), et le résultat attendu calculé.
3. Au minimum les cas demandés par l'US2 : quorum (atteint, non atteint, exactement au seuil), majorité (adoptée, rejetée, égalité), chaque profil, adoption sans fonds suffisants, reproductibilité avec une même graine.
4. Les cas limites issus des zones floues tranchées dans la spec (bâtiment qui rapporte au tour suivant, trésorerie à exactement 0, victoire en fin de tour 30, etc.).
5. Comment tu testeras l'absentéiste, dont le vote est aléatoire, sans obtenir des tests qui passent ou échouent au hasard.
6. Les documents à mettre à jour (README, CLAUDE.md, backlog).

Explique-le simplement : je dois comprendre chaque cas sans connaître Python.
```

**Pourquoi ce prompt**
- **Les « règles impératives »** posent la séparation entre ce qu'on vérifie (le code) et la référence (la spec).
- **Le tableau du point 2** rend chaque test traçable jusqu'à une règle de la spec : je peux relire les tests sans lire de Python.
- **Le point 5** anticipe un piège classique : un test qui dépend du hasard peut réussir un jour et échouer le lendemain.

### Étape 2 — Relire le plan

Quatre questions :
1. **Traçabilité** : chaque cas cite-t-il une règle de la spec ?
2. **Valeurs attendues** : je reprends deux ou trois cas et je refais le calcul moi-même. Est-ce juste ?
3. **Couverture** : tous les cas demandés par l'US2 et toutes les zones floues tranchées y sont-ils ?
4. **Périmètre** : aucun fichier de `src/` n'est modifié ?

J'approuve quand tout est bon, en validant les modifications une par une.

### Étape 3 — Lancer les tests

Claude donne la commande à la fin. Je la lance moi-même, dans le terminal :

```bash
python3 -m unittest discover -s tests -v
```

(La commande exacte peut différer : c'est celle que Claude aura documentée qui fait foi.)

- **Tout est `ok`** : le code respecte la spec, pour tous les cas testés.
- **Un test échoue** : c'est une information précieuse, pas un problème. Je lis le message, puis je demande à Claude de m'expliquer l'écart. Ensuite je tranche : soit le code est faux (on le corrige), soit la spec est floue ou fausse (je la corrige, puis le test).

### Étape 4 — Casser exprès

Le meilleur moyen de croire en ses tests est de les voir attraper une erreur.

1. Demander à Claude, en mode normal (`Maj + Tab` pour sortir du mode plan) :

```
Ne modifie rien. Montre-moi le fichier et la ligne exacte où la règle de majorité « strictement plus de 50 % » est appliquée, et explique-la-moi.
```

2. Ouvrir ce fichier dans VS Code, et **modifier moi-même la règle** : remplacer « strictement plus de 50 % » par « 50 % ou plus ». Dans le code, c'est souvent remplacer `>` par `>=`. Enregistrer.
3. Relancer les tests. Au moins un test doit échouer : celui de l'égalité. Lire son message : comprend-on ce qui ne va pas ?
4. Réparer avec git :

```bash
git restore src/partie.py
```

(Adapter le nom du fichier si la règle est ailleurs.)

5. Relancer les tests : tout repasse au vert.

### Étape 5 — Ancrer les tests dans la méthode

Vérifier que Claude a bien mis à jour :
- le `README.md` : la commande des tests ;
- le `CLAUDE.md` : la commande des tests, et une règle du type « avant de déclarer une tâche terminée, lance tous les tests : ils doivent tous passer ; ne modifie jamais un test pour le faire passer sans mon accord » ;
- le `docs/backlog.md` : l'US2 à « Terminé ».

Si ce n'est pas fait, le lui demander.

### Étape 6 — Commit

```bash
git status
```

```bash
git diff
```

```bash
git add .
```

```bash
git commit -m "US2 : tests des règles de vote"
```

```bash
git push
```

### Étape 7 — Journal

À noter : les écarts éventuels trouvés par les tests, l'expérience « casser exprès », et ce qu'elle m'a appris sur la confiance que je peux accorder au code de l'agent.

---

## 6. Ce que ça change pour un PO

- **Les tests sont des critères d'acceptation exécutables.** Une règle de la spec devient une vérification qui tourne toute seule, à chaque modification.
- **La traçabilité spec → test** permet de relire une suite de tests sans lire de code : chaque test répond à une règle.
- **L'agent ne note pas sa propre copie.** Des tests dérivés de la spec sont indépendants du code qu'ils vérifient.
- **Un test rouge est une information, pas un échec.** Il dit qu'il y a un écart ; au PO de décider qui a raison.
- **Interdire de modifier un test pour le faire passer** est une règle de gouvernance du code, à écrire noir sur blanc dans le `CLAUDE.md`.

---

## 7. Les pièges

- **Des tests écrits en lisant le code** : ils valident les bugs au lieu de les trouver.
- **Laisser Claude « corriger » un test rouge** en changeant la valeur attendue : c'est effacer le thermomètre parce qu'on a de la fièvre.
- **Des tests dépendant du hasard** : ils passent un jour, échouent le lendemain, et on finit par les ignorer.
- **Beaucoup de tests, peu de valeur** : dix tests du dépensier qui vote toujours oui ne valent pas un test de l'égalité à 50 %.
- **Oublier `git restore` après l'exercice « casser exprès »**, et committer la règle cassée. `git diff` avant chaque commit protège de ça.

---

## Checklist de fin de leçon

- [ ] chaque cas de test cite une règle de la spec
- [ ] j'ai recalculé moi-même au moins deux valeurs attendues
- [ ] tous les tests passent avec la commande documentée
- [ ] j'ai cassé une règle, vu un test échouer, et réparé avec `git restore`
- [ ] `README.md`, `CLAUDE.md` et le backlog sont à jour
- [ ] le commit est envoyé sur GitHub
- [ ] l'entrée de journal est écrite

**Prochaine leçon** : US3, les réglages dans un fichier. Les tests vont servir pour la première fois de filet de sécurité pendant une vraie modification du code.
