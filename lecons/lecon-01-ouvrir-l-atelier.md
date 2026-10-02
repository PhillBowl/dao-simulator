# Leçon 1 — Ouvrir l'atelier au public

> Version V0 (suite) · Durée estimée : une à deux sessions de 2 heures

---

## 1. Ce qu'on va faire

Publier le projet sur GitHub, avec tout ce qu'un dépôt public sérieux doit contenir : une présentation (`README.md`), une licence (`LICENSE`), les documents du projet, et surtout un premier **`CLAUDE.md`**, le fichier qui explique à Claude les règles du projet au début de chaque session.

---

## 2. Le concept

### Dépôt local, dépôt distant

Jusqu'ici, l'album photo (l'historique git) n'existe que sur mon Mac. On va en créer une copie sur GitHub :

| | Où | Rôle |
|---|---|---|
| **Dépôt local** | `~/dao-simulator` sur mon Mac | Là où je travaille, avec Claude |
| **Dépôt distant** | github.com/PhillBowl/dao-simulator | La vitrine publique, et une sauvegarde |

Deux mots à connaître :
- **push** : envoyer mes nouveaux commits du Mac vers GitHub ;
- **remote** : le nom que git donne au dépôt distant, par convention `origin`.

Seuls les commits partent sur GitHub. Ce que le `.gitignore` exclut (le journal, les secrets) reste sur le Mac.

### Les fichiers d'un dépôt public

| Fichier | Pour qui | Rôle |
|---|---|---|
| `README.md` | Les visiteurs | La page d'accueil du projet : ce que c'est, où il en est, comment le lancer |
| `LICENSE` | Les visiteurs et contributeurs | Ce qu'ils ont le droit de faire avec le code |
| `CLAUDE.md` | Claude | Les règles du projet, lues automatiquement au début de chaque session |

### Le `CLAUDE.md`

Chaque session de Claude Code démarre avec une mémoire vide. Le `CLAUDE.md`, placé à la racine du projet, est lu automatiquement à chaque démarrage. C'est l'endroit où l'on écrit ce qu'on devrait sinon répéter à chaque fois.

Ce que recommande la documentation de Claude Code :
- **rester court** : moins de 200 lignes. Plus il est long, moins il est bien suivi ;
- **être concret et vérifiable** : « lance `python3 vote.py` pour vérifier » plutôt que « vérifie ton travail » ;
- **l'organiser** avec des titres et des listes ;
- **le faire évoluer** : on y ajoute une règle quand Claude commet deux fois la même erreur, ou quand on se surprend à répéter la même consigne.

À savoir : le `CLAUDE.md` guide Claude, mais il ne l'oblige pas. Pour imposer une règle quoi qu'il arrive, il existe les *hooks* (V3).

---

## 3. Pourquoi maintenant

- Le cadrage prévoit un dépôt public dès le départ.
- Sans `CLAUDE.md`, je devrais réexpliquer le projet, mon niveau et les conventions à chaque session. C'est la première brique de la chaîne vision → spec → backlog → instructions à l'agent.
- Plus tôt la licence est posée, plus tôt les règles du jeu sont claires pour les visiteurs.

---

## 4. Les outils

- **GitHub CLI (`gh`)** : un outil en ligne de commande qui pilote GitHub depuis le terminal. Il crée le dépôt en ligne et gère la connexion en une commande.
- **Dans Claude Code** :
  - `/context` affiche ce que Claude a chargé, dont les fichiers `CLAUDE.md` (rubrique *Memory files*) ;
  - `/memory` permet d'ouvrir et de modifier ces fichiers ;
  - `/init` génère un `CLAUDE.md` automatiquement à partir du code. Sur un projet d'un seul fichier, il aurait peu à dire : on écrit donc le nôtre.

---

## 5. L'exercice, pas à pas

### Étape 1 — Ranger les documents du projet

Créer les dossiers :

```bash
cd ~/dao-simulator
```

```bash
mkdir docs lecons
```

Télécharger depuis la conversation avec Claude le document de cadrage et la leçon 0, puis les déplacer (adapter le nom si le fichier téléchargé s'appelle autrement) :

```bash
mv ~/Downloads/dao-simulator-v1.md docs/cadrage.md
```

```bash
mv ~/Downloads/lecon-00-preparer-son-atelier.md lecons/
```

Vérifier :

```bash
ls docs lecons
```

**Relire avant de publier** : ces documents seront publics. Le cadrage cite mon mémoire et le prénom d'Alex. Est-ce que tout me convient ? Si non, je modifie avant le commit.

### Étape 2 — Installer GitHub CLI et se connecter

```bash
brew install gh
```

```bash
gh auth login
```

Répondre aux questions avec les flèches et Entrée :
- *Where do you use GitHub?* → **GitHub.com**
- *Preferred protocol for Git operations?* → **HTTPS**
- *Authenticate Git with your GitHub credentials?* → **Yes**
- *How would you like to authenticate?* → **Login with a web browser**

Un code s'affiche : le copier, appuyer sur Entrée, le coller dans la page qui s'ouvre, valider. Vérifier :

```bash
gh auth status
```

### Étape 3 — README et LICENSE avec Claude

Lancer Claude dans le dossier du projet :

```bash
claude
```

**Cette fois, j'écris le prompt moi-même**, avec la grille :

| Élément | Ce que mon prompt doit dire |
|---|---|
| Contexte | Le projet est sur le point d'être publié sur GitHub ; le cadrage est dans `docs/cadrage.md` |
| Objectif | Deux fichiers : `README.md` et `LICENSE` |
| Contenu du README | Le pitch en une phrase, les trois objectifs, l'état actuel (V0 : un seul vote simulé), comment lancer le programme, l'organisation des dossiers, les licences |
| Licences | MIT pour le code, au nom de PhillBowl, année 2026 ; Creative Commons BY 4.0 pour les textes (documentation, leçons), mentionnée dans le README |
| Contraintes | En français ; court et sobre ; ne rien promettre que le projet ne fait pas encore ; ne pas mentionner le journal (privé) |
| Façon de travailler | Lire le cadrage avant d'écrire ; me montrer le README avant de l'enregistrer ; ne pas faire de commit |
| Critère de fin | Les deux fichiers existent, et Claude signale ses choix non demandés |

Une proposition figure en annexe A, **à lire seulement après avoir envoyé mon prompt**.

Relire le README dans VS Code (`code README.md`) : est-ce qu'il décrit fidèlement le projet ? Demander les corrections nécessaires.

### Étape 4 — Écrire le `CLAUDE.md`

Toujours dans la session Claude. Mon prompt doit demander un `CLAUDE.md` **de moins de 80 lignes**, organisé en rubriques :

| Rubrique | Ce qu'elle contient |
|---|---|
| Le projet | Deux ou trois phrases, et un renvoi vers `docs/cadrage.md` |
| Qui je suis | Débutant complet en Python et git, PO de métier ; j'apprends en construisant |
| Comment travailler avec moi | Résumer avant d'écrire ; expliquer simplement ; signaler les choix non demandés ; ne jamais committer sans que je le demande |
| Coaching de prompts | Avant une tâche importante, un retour court sur mon prompt : ce qui marche, ce qui manque, une structure proposée |
| Conventions de code | Python, bibliothèque standard uniquement ; tout en français (commentaires, noms, affichages) ; réglages en constantes en haut des fichiers ; petites fonctions ; lisible plutôt que court ; graine aléatoire fixe |
| Organisation des dossiers | Rôle de `docs/`, `lecons/`, `journal/`, puis plus tard `src/`, `tests/`, `config/` |
| Sécurité | Aucun secret dans le dépôt ; ne jamais lire ni modifier `journal/`, qui est privé |
| Commandes | Comment lancer le programme |

Une proposition figure en annexe B, à lire après avoir envoyé mon prompt.

Relire le `CLAUDE.md` ligne par ligne. **C'est mon contrat de travail avec l'agent** : chaque règle doit être une règle que je veux vraiment.

### Étape 5 — Vérifier que Claude lit le `CLAUDE.md`

Quitter Claude (`/exit`), le relancer (`claude`), puis taper :

```
/context
```

Le `CLAUDE.md` doit apparaître dans la rubrique *Memory files*. Puis demander :

```
Quelles sont les règles de ce projet, et comment dois-tu travailler avec moi ?
```

La réponse doit reprendre mes règles, sans que je les aie redites.

### Étape 6 — Commit

Quitter Claude, puis, dans le terminal, une commande à la fois :

```bash
git status
```

Vérifier la liste : `README.md`, `LICENSE`, `CLAUDE.md`, `docs/`, `lecons/`. **Le journal ne doit pas apparaître.**

```bash
git add README.md LICENSE CLAUDE.md docs lecons
```

```bash
git commit -m "README, licence, CLAUDE.md et documents du projet"
```

### Étape 7 — Créer le dépôt sur GitHub et publier

```bash
gh repo create dao-simulator --public --source=. --remote=origin --push
```

En une commande : création du dépôt public sur GitHub, enregistrement du remote `origin`, envoi de tous les commits.

Ouvrir le dépôt dans le navigateur :

```bash
gh repo view --web
```

Vérifier sur la page :
- le README s'affiche en page d'accueil ;
- GitHub reconnaît la licence MIT (affichée dans la colonne de droite) ;
- **le dossier `journal/` est absent** ;
- l'historique compte quatre commits.

### Étape 8 — Journal

Écrire l'entrée de la session dans `journal/`, moi-même cette fois.

---

## 6. Ce que ça change pour un PO

- **Le `CLAUDE.md` est un accord de travail**, comme la charte d'une équipe agile ou sa *definition of done*. Il se négocie une fois, se relit souvent, et évolue quand la pratique révèle un manque.
- **Une règle vague n'est pas une règle.** « Code propre » ne veut rien dire pour un agent ; « une fonction = un rôle, constantes en haut du fichier » se vérifie.
- **Le README est la vision produit publique.** Il doit dire ce que le produit fait aujourd'hui, pas ce qu'il fera un jour.
- **La licence est une règle de gouvernance** : elle fixe ce que les autres peuvent faire de mon travail.
- **Publier, c'est relire.** Avant tout push public, je vérifie ce qui part : personne d'autre ne le fera pour moi.

---

## 7. Les pièges

- **Publier sans relire** : un prénom, un détail personnel, une phrase datée.
- **Un `CLAUDE.md` trop long ou trop vague** : il sera mal suivi.
- **Des règles contradictoires** dans le `CLAUDE.md` : Claude en choisit une au hasard.
- **Croire que le `CLAUDE.md` est une barrière** : c'est une consigne, pas un verrou. Pour le journal, le `.gitignore` reste la vraie protection côté publication.
- **Un README qui survend** : « simulateur de gouvernance de Metz » alors que le projet simule un seul vote.
- **Oublier le `--public`** : le dépôt serait créé en privé.

---

## Checklist de fin de leçon

- [ ] `docs/cadrage.md` et `lecons/lecon-00-…` sont dans le projet, relus
- [ ] `gh auth status` confirme la connexion à GitHub
- [ ] `README.md` et `LICENSE` existent et décrivent fidèlement le projet
- [ ] `CLAUDE.md` existe, fait moins de 80 lignes, et apparaît dans `/context`
- [ ] Claude restitue mes règles sans que je les redise
- [ ] le dépôt public est en ligne, sans le journal
- [ ] l'entrée de journal est écrite par moi

**Prochaine leçon** : passer de V0 à V1 en écrivant ma première spec de version, puis découvrir le mode plan.

---

## Annexe A — Proposition de prompt : README et LICENSE

*À lire après avoir envoyé le mien.*

> Le projet va être publié sur GitHub, en dépôt public. Lis d'abord `docs/cadrage.md` pour comprendre le projet.
>
> Crée deux fichiers :
>
> 1. `README.md`, la page d'accueil du dépôt, en français, court et sobre :
>    - le pitch en une phrase, repris du cadrage ;
>    - les trois objectifs du projet ;
>    - l'état actuel : V0, un programme qui simule un seul vote de DAO ;
>    - comment lancer le programme ;
>    - l'organisation des dossiers ;
>    - les licences : MIT pour le code (fichier `LICENSE`), Creative Commons BY 4.0 pour les textes (documentation et leçons), avec un lien vers la licence CC BY 4.0.
>
>    Ne promets rien que le projet ne fait pas encore. Ne mentionne pas le dossier `journal/`, qui est privé.
>
> 2. `LICENSE` : le texte standard de la licence MIT, au nom de PhillBowl, année 2026.
>
> Montre-moi le README avant de l'enregistrer. Ne fais aucun commit. À la fin, signale les choix que tu as faits sans que je les précise.

## Annexe B — Proposition de prompt : CLAUDE.md

*À lire après avoir envoyé le mien.*

> Crée le fichier `CLAUDE.md` du projet, en français, en moins de 80 lignes. Il sera lu au début de chaque session : chaque règle doit être concrète et vérifiable. Organise-le avec ces rubriques :
>
> - **Le projet** : deux ou trois phrases, et un renvoi vers `docs/cadrage.md` pour le détail.
> - **Qui je suis** : PO de métier, débutant complet en Python et en git. J'apprends en construisant ce projet avec toi.
> - **Comment travailler avec moi** : avant d'écrire du code, résume en quelques lignes ce que tu vas faire ; explique simplement, sans jargon non défini ; à la fin d'une tâche, signale les choix que tu as faits sans que je les précise ; ne fais jamais de commit sans que je le demande.
> - **Coaching de prompts** : avant une tâche importante (nouvelle fonctionnalité, modification de plusieurs fichiers), donne un retour court sur mon prompt : ce qui marche, ce qui manque (contexte, objectif, contraintes, format, critère de fin), une structure proposée. Ne réécris pas le prompt à ma place.
> - **Conventions de code** : Python, bibliothèque standard uniquement sauf décision explicite ; tout en français (commentaires, noms de variables et de fonctions, textes affichés) ; réglages en constantes en haut des fichiers ; petites fonctions avec un seul rôle ; code lisible plutôt que court ; graine aléatoire fixe pour des résultats reproductibles.
> - **Organisation des dossiers** : `docs/` (cadrage, specs), `lecons/` (leçons publiques), `journal/` (privé) ; plus tard `src/`, `tests/`, `config/`.
> - **Sécurité** : aucun secret (clé d'API, mot de passe) dans le dépôt ; ne lis et ne modifie jamais le dossier `journal/`.
> - **Commandes** : lancer le programme avec `python3 vote.py`.
>
> Montre-moi le fichier avant de l'enregistrer. Ne fais pas de commit.
