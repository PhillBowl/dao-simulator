# Leçon 0 — Préparer son atelier

> Version V0 · Durée estimée : deux sessions de 2 à 3 heures

---

## 1. Ce qu'on va faire

Installer les outils sur le Mac, puis écrire avec Claude Code un premier mini-programme : **un seul vote de DAO**, avec quorum et majorité. À la fin, ce programme est enregistré dans git et je sais expliquer chacune de ses lignes.

---

## 2. Le concept : cinq outils, cinq rôles

| Outil | Ce que c'est | Image |
|---|---|---|
| **Terminal** | Une fenêtre où l'on donne des ordres à l'ordinateur en les tapant, au lieu de cliquer | Parler à l'ordinateur par écrit |
| **Python** | Le langage dans lequel le simulateur sera écrit. Un fichier `.py` contient des instructions que Python exécute | La langue dans laquelle on écrit la recette |
| **Git** | Un logiciel qui garde l'historique de toutes les versions du projet. Chaque enregistrement s'appelle un *commit* | Un appareil photo : chaque commit est une photo du projet à un instant donné, et on peut toujours revenir à une photo précédente |
| **GitHub** | Le site qui héberge le projet en ligne, visible de tous | La vitrine publique de l'atelier |
| **Claude Code** | Un agent qui travaille dans le terminal, dans le dossier du projet. Il lit les fichiers, en écrit, lance des commandes, et demande la permission avant d'agir | Un développeur à qui je confie des tâches, et dont je relis le travail |

Deux outils de confort s'ajoutent :

- **Homebrew** : un installateur de logiciels pour Mac. Il installe Python et les autres outils en une commande.
- **Visual Studio Code** (VS Code) : un éditeur de texte fait pour lire du code, avec des couleurs qui rendent la structure lisible. Indispensable pour relire ce que Claude écrit.

---

## 3. Pourquoi maintenant

Tout le reste du projet repose sur ces outils. Et surtout, la première chose à apprendre n'est pas Python : c'est **le cycle de travail avec un agent**. Je décris ce que je veux, Claude le fait, je relis, je lance, je comprends, j'enregistre. Ce cycle va se répéter des centaines de fois. Autant le pratiquer tout de suite sur un exemple minuscule.

---

## 4. L'outil Claude Code : comment ça marche

- **On le lance depuis le dossier du projet**, en tapant `claude` dans le terminal. Il ne voit que ce dossier et ses sous-dossiers.
- **On lui parle en français**, comme dans une conversation.
- **Il demande la permission** avant de créer un fichier, de le modifier ou de lancer une commande. Chaque demande s'affiche à l'écran : je la lis avant d'accepter. C'est mon principal moyen de contrôle.
- **On peut l'interrompre** avec la touche Échap s'il part dans une mauvaise direction.
- **On quitte** en tapant `/exit`.
- **`/help`** affiche les commandes disponibles.

Claude Code est inclus dans l'abonnement Pro. Au premier lancement, il ouvre le navigateur pour se connecter avec mon compte Claude.

---

## 5. L'exercice, pas à pas

### Étape 1 — Ouvrir le terminal et faire ses premiers pas

Ouvrir le terminal : `Cmd + Espace`, taper « Terminal », Entrée.

Essayer ces commandes, une par une, en appuyant sur Entrée après chacune :

| Commande | Ce qu'elle fait |
|---|---|
| `pwd` | Affiche le dossier où je me trouve |
| `ls` | Liste ce qu'il contient |
| `cd Documents` | Entre dans le dossier Documents |
| `cd ..` | Remonte d'un dossier |
| `cd ~` | Revient au dossier personnel |

Astuce : la touche Tab complète automatiquement les noms de dossiers.

### Étape 2 — Installer les outils de développement d'Apple (dont git)

```bash
xcode-select --install
```

Une fenêtre s'ouvre : accepter. Si un message indique que c'est déjà installé, passer à la suite. Vérifier :

```bash
git --version
```

Un numéro de version s'affiche : git est installé.

### Étape 3 — Installer Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Le mot de passe du Mac est demandé (rien ne s'affiche quand on le tape, c'est normal). **À la fin, Homebrew affiche une rubrique « Next steps » avec deux ou trois commandes à copier-coller : les exécuter**, sinon la commande `brew` ne sera pas reconnue. Vérifier :

```bash
brew --version
```

### Étape 4 — Installer Python et VS Code

```bash
brew install python
brew install --cask visual-studio-code
```

Vérifier :

```bash
python3 --version
```

Sur Mac, on tape toujours `python3`, pas `python`.

### Étape 5 — Installer Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Ouvrir une nouvelle fenêtre de terminal** (`Cmd + N`), puis vérifier :

```bash
claude --version
```

### Étape 6 — Se présenter à git

Git signe chaque commit avec un nom et un email. Une seule fois :

```bash
git config --global user.name "Pierre Bouard"
git config --global user.email "mon-email@exemple.com"
```

Utiliser l'email du futur compte GitHub.

### Étape 7 — Créer un compte GitHub

Sur github.com. Le dépôt en ligne sera créé à la leçon 1 : pour l'instant, le compte suffit.

### Étape 8 — Créer le dossier du projet

```bash
mkdir ~/dao-simulator
cd ~/dao-simulator
git init
```

`git init` transforme ce dossier en projet suivi par git. Il est encore vide.

### Étape 9 — Première session avec Claude Code

Toujours dans le dossier `dao-simulator` :

```bash
claude
```

Se connecter dans le navigateur quand il le demande.

### Étape 10 — Écrire mon premier prompt

**C'est l'étape la plus importante.** Je rédige moi-même la demande, en suivant la grille du cadrage :

| Élément | Ce que mon prompt doit dire |
|---|---|
| Contexte | Qui je suis (débutant complet), ce qu'est le projet en deux phrases |
| Objectif | Deux fichiers : un `.gitignore` qui protège les secrets, et un programme `vote.py` qui simule un seul vote de DAO |
| Les règles du vote | 10 membres avec 100 tokens chacun ; chacun vote oui, non ou s'abstient, au hasard ; quorum de 40 % des tokens ; adoption si plus de 50 % de oui parmi les votes exprimés |
| Contraintes | Python simple, sans bibliothèque à installer ; une graine aléatoire fixée pour que le résultat soit reproductible ; des commentaires en français sur chaque ligne ; un code fait pour être lu par un débutant |
| Format de sortie | Ce que le programme doit afficher : le vote de chaque membre, la participation, le résultat |
| Critère de fin | Le programme tourne avec `python3 vote.py`, et Claude m'explique comment le lancer |

Écrire le prompt, l'envoyer, puis **lire chaque demande de permission avant d'accepter**.

Une proposition de prompt figure en annexe. **Ne la lire qu'après avoir écrit et envoyé le mien**, pour comparer.

### Étape 11 — Lancer le programme

Ouvrir un second terminal (`Cmd + T` crée un nouvel onglet), aller dans le dossier, lancer :

```bash
cd ~/dao-simulator
python3 vote.py
```

Le relancer plusieurs fois : le résultat est identique, grâce à la graine. Puis demander à Claude de changer la graine, et relancer.

### Étape 12 — Lire et comprendre

1. Ouvrir le dossier dans VS Code : `code .` dans le terminal (ou ouvrir VS Code et glisser le dossier dedans).
2. Lire `vote.py` du début à la fin.
3. Pour chaque ligne incomprise, demander à Claude : « explique-moi la ligne X comme à un débutant ».
4. **Modifier moi-même le quorum** dans le fichier (passer de 40 % à 70 %), enregistrer, relancer. Le résultat change-t-il ? Pourquoi ?
5. Remettre 40 %.

L'étape est validée quand je peux expliquer à voix haute ce que fait chaque bloc du programme.

### Étape 13 — Premier commit

Dans le terminal (pas dans Claude) :

```bash
git status
git add .gitignore vote.py
git commit -m "Premier vote de DAO simulé"
git log
```

| Commande | Ce qu'elle fait |
|---|---|
| `git status` | Montre ce qui a changé depuis la dernière photo |
| `git add` | Choisit les fichiers à mettre dans la prochaine photo |
| `git commit -m "..."` | Prend la photo, avec une légende |
| `git log` | Affiche l'album des photos |

### Étape 14 — Première entrée du journal de bord

Créer un fichier `journal/2026-10-xx.md` (avec la date du jour) contenant :

- l'objectif de la session ;
- mon prompt de l'étape 10, tel que je l'ai envoyé ;
- ce qui a marché, ce qui a bloqué ;
- ce que j'ai appris ;
- une chose que je ferais différemment.

Le journal est **privé** : il ne doit jamais être publié. Ajouter la ligne `journal/` à la fin du fichier `.gitignore`, enregistrer, puis vérifier avec `git status` que le dossier n'apparaît plus. Committer seulement la modification du `.gitignore` :

```bash
git add .gitignore
git commit -m "Le journal de bord reste privé"
```

---

## 6. Ce que ça change pour un PO

- **Installer l'environnement, c'est faire l'onboarding de l'agent.** Comme pour un nouveau développeur : on lui donne un espace de travail, un périmètre (le dossier) et des droits (les permissions).
- **Les demandes de permission sont un outil de gouvernance.** Les accepter sans les lire revient à valider une mise en production sans recette.
- **Le prompt est un ticket.** Contexte, objectif, contraintes, critère d'acceptation : c'est une user story, adressée à un agent.
- **Le commit est l'incrément.** Chaque étape validée est enregistrée et traçable, et on peut toujours revenir en arrière.
- **Le `.gitignore` est de la sécurité dès la conception** : on protège les secrets avant d'en avoir.

---

## 7. Les pièges

- **Coller des commandes sans les lire.** Les commandes `curl … | bash` installent un logiciel depuis Internet : ne les utiliser que depuis des sources officielles, comme ici.
- **Accepter toutes les permissions sans lire.** Surtout celles qui suppriment des fichiers ou lancent des commandes.
- **« command not found »** juste après une installation : ouvrir une nouvelle fenêtre de terminal. Pour Homebrew, vérifier que les commandes « Next steps » ont bien été exécutées.
- **Taper `python` au lieu de `python3`.**
- **Lancer `claude` hors du dossier du projet** : il travaillerait au mauvais endroit.
- **Valider un code non compris.** Règle n° 2 du cadrage : on demande une explication avant d'accepter.
- **Commiter un secret.** Une fois sur GitHub, même supprimé ensuite, il reste dans l'historique.

---

## Checklist de fin de leçon

- [ ] `git --version`, `brew --version`, `python3 --version` et `claude --version` affichent tous un numéro de version
- [ ] le dossier `~/dao-simulator` est un dépôt git
- [ ] `python3 vote.py` affiche un vote complet, identique à chaque lancement
- [ ] j'ai modifié le quorum moi-même et compris l'effet
- [ ] je sais expliquer chaque bloc de `vote.py`
- [ ] deux commits existent : le programme, puis l'exclusion du journal
- [ ] le journal, privé, contient mon premier prompt

**Prochaine leçon** : créer le dépôt sur GitHub, y publier le projet, et écrire le premier `CLAUDE.md`.

---

## Annexe — Une proposition de prompt

*À lire seulement après avoir écrit et envoyé le mien.*

> Je débute complètement en programmation : je n'ai jamais écrit de Python. Je construis un simulateur de DAO (organisation autonome décentralisée) pour apprendre à développer avec toi.
>
> Pour commencer, crée deux fichiers dans ce dossier :
>
> 1. Un `.gitignore` qui exclut de git les fichiers de secrets (`.env`, clés d'API) et les fichiers temporaires de Python et de macOS.
> 2. Un programme `vote.py` qui simule un seul vote de DAO :
>    - 10 membres, avec 100 tokens chacun ;
>    - chaque membre vote oui, non ou s'abstient, au hasard ;
>    - le vote est valide si au moins 40 % des tokens ont voté (quorum) ;
>    - la proposition est adoptée si plus de 50 % des votes exprimés sont des oui.
>
> Contraintes : Python simple, sans bibliothèque à installer. Fixe une graine aléatoire pour que le résultat soit identique à chaque lancement. Commente chaque ligne en français, pour un débutant. Préfère un code lisible à un code court.
>
> Le programme doit afficher le vote de chaque membre, le taux de participation, si le quorum est atteint, et le résultat final.
>
> Quand c'est fait, dis-moi comment le lancer et résume en quelques phrases ce que fait chaque partie du programme.
