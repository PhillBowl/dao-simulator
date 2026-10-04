# DAO Simulator — Document de cadrage

> Statut : cadrage consolidé · Version 1.0 · 01/10/2026

**En une phrase** : un laboratoire open source pour tester, partie après partie, quelles règles permettraient à une DAO de gouverner une ville comme Metz, construit pour apprendre le métier de PO avec des agents.

**Plan**

- Partie 1 — Le projet : §1 à §2
- Partie 2 — Comprendre les DAO : §3 à §4
- Partie 3 — Le simulateur : §5 à §11
- Partie 4 — La démarche : §12 à §18
- Sources

---

# Partie 1 — Le projet

## 1. Pourquoi ce projet

Trois objectifs :

1. **Apprendre à développer avec Claude Code**, progressivement, jusqu'à maîtriser les usages avancés (agents, hooks, skills, travail en parallèle).
2. **Comprendre comment fonctionne une DAO** en en construisant une, puis en observant ce qui la fait réussir ou échouer.
3. **Devenir un PO qui sait travailler avec des agents.** Pouvoir dire, preuves à l'appui : « voilà comment je rédige une spec pour un agent, comment je découpe le travail, comment je relis, comment je décide ».

Le troisième objectif fixe la priorité : le livrable le plus précieux n'est pas le simulateur, c'est **la méthode**, documentée au fil de l'eau.

Il n'y a pas de ligne d'arrivée. Le projet explore des concepts de plus en plus poussés, côté gouvernance comme côté développement avec agents. On commence minuscule et on ajoute une brique à la fois.

Le projet prolonge mon mémoire de master (ESCP, 2019), *Morphological Analysis of a viable DAO* (§4).

## 2. Le cadre du projet

### 2.1 Point de départ

- Je n'ai jamais codé en Python ni utilisé git.
- Je travaille sur Mac.
- J'utilise Claude Code en local, dans le terminal.

Les leçons partent donc de zéro (§12), et une version V0 est consacrée à l'installation et aux bases.

### 2.2 Ce que le projet n'est pas

- **Pas un projet blockchain** : aucun smart contract, aucune crypto. Tout est simulé.
- **Pas un outil réel pour la mairie** : Metz est un terrain d'expérience, pas un client.
- **Pas un jeu commercial** : le but est d'apprendre et de comprendre, pas de vendre.
- **Pas un modèle prédictif** : le simulateur explore des mécanismes sous hypothèses, il ne prédit pas ce que feraient de vrais habitants.

### 2.3 Les arbitrages

Quand le temps manque ou que deux objectifs s'opposent, voici l'ordre, du plus protégé au premier sacrifié :

1. **Apprendre le métier de PO avec des agents.** Mieux vaut une petite version comprise et documentée qu'une grosse version subie.
2. **Le réalisme du modèle.** Un petit modèle crédible vaut mieux qu'un grand modèle approximatif.
3. **Le périmètre.** Faire moins, mais bien.
4. **La vitesse.** Il n'y a pas de deadline.

---

# Partie 2 — Comprendre les DAO

## 3. C'est quoi une DAO ?

### 3.1 L'idée en une phrase

Une **DAO** (*Decentralized Autonomous Organization*, organisation autonome décentralisée) est un groupe de personnes qui gèrent une caisse commune et prennent leurs décisions par des votes dont les règles sont écrites dans du code.

### 3.2 Les trois ingrédients

Une organisation est une DAO si elle réunit les trois :

- **Une gouvernance décentralisée** : personne ne décide seul, les choix passent par un vote.
- **De l'automatisation au centre** : les règles s'appliquent toutes seules, sans chef pour les faire respecter. Les humains restent « au bord », pour faire ce que le code ne sait pas faire.
- **Un capital commun** : une trésorerie que la DAO dépense selon ses votes.

### 3.3 L'analogie de l'association

| Dans une association classique | Dans une DAO |
|---|---|
| Les statuts sont écrits sur papier | Les règles sont écrites dans un programme (un *smart contract*) |
| Le trésorier garde la caisse | La caisse est bloquée dans le programme : personne ne peut la toucher seul |
| On vote à main levée en assemblée | On vote en ligne, chacun avec ses *tokens* |
| Le bureau applique la décision | Le programme applique la décision automatiquement si le vote passe |

La différence clé : **dans une DAO, personne n'a besoin de faire confiance à un président ou à un trésorier.** Le code fait ce que les votes ont décidé, rien de plus, rien de moins.

### 3.4 Les mots à connaître

- **Membre** : une personne qui participe à la DAO.
- **Token** (jeton) : une part de la DAO. Posséder des tokens donne le droit de voter. En général, **1 token = 1 voix**.
- **Réputation** : une alternative au token. Elle se gagne en contribuant, ne s'achète pas et ne se revend pas.
- **Trésorerie** : l'argent commun de la DAO.
- **Proposition** : une idée soumise au vote (« dépensons 200 pour construire un atelier »).
- **Quorum** : le minimum de participation pour que le vote compte.
- **Majorité** : la part de « oui » nécessaire pour adopter la proposition, parmi les votes exprimés.
- **Délégation** : confier sa voix à quelqu'un d'autre, en pouvant la reprendre à tout moment.
- **Exécution** : l'application automatique d'une proposition adoptée.

### 3.5 Pourquoi c'est difficile de faire une DAO qui marche

- **L'absentéisme** : la plupart des membres ne votent pas. Le quorum n'est pas atteint, rien n'avance.
- **Les baleines** : quelques membres possèdent la majorité des tokens et décident seuls. C'est une ploutocratie, pas une démocratie.
- **La lenteur** : tout voter prend du temps.
- **Les attaques** : quelqu'un emprunte ou achète massivement des tokens juste avant un vote pour vider la caisse.
- **Les bugs** : en 2016, « The DAO » s'est fait détourner une grande partie de sa trésorerie à cause d'une faille dans son code.

## 4. Le mémoire et l'état de l'art

### 4.1 Ce qui reste valable dans le mémoire

Le cœur du mémoire tient toujours : **la liste des questions qu'une DAO ne peut pas esquiver** (son tableau 4). Nombre de votants, nature des votes, délégation, durée des votes, seuils différenciés selon l'importance des décisions, protection des minorités, incitations, identité. Les sept années suivantes n'ont pas ajouté de question majeure ; elles ont surtout montré lesquelles faisaient le plus mal en pratique.

Deux constats ont été largement confirmés :

- **La participation est le problème numéro un.** Dans la plupart des grandes DAO, une petite fraction des tokens vote.
- **La critique de Vlad Zamfir** (la gouvernance est un processus, pas un design) est devenue centrale. Les DAO qui durent sont celles qui modifient leurs règles en marchant.

### 4.2 Ce qui a vieilli

- **Les cas étudiés** : plusieurs ont fermé ou profondément changé. DigixDAO s'est dissoute en 2020, l'association Aragon a été dissoute en 2023, MakerDAO est devenue Sky en 2024.
- **Le vote par réputation**, présenté comme la cible de la plupart des projets, est resté marginal. En pratique, le vote par token avec **délégation** s'est imposé.
- **On-chain contre off-chain** : le débat s'est résolu en modèle hybride. On discute et on vote hors blockchain, puis l'exécution passe par un délai de sécurité et un portefeuille multi-signatures.
- **Le cadre juridique** : il existe désormais des statuts légaux pour les DAO dans certains États américains et aux îles Marshall.
- **Les mineurs** : Ethereum ne fonctionne plus par minage depuis 2022.

### 4.3 Ce qui est apparu depuis

- **Les attaques de gouvernance** : emprunter massivement des tokens le temps d'un vote pour vider une caisse. Ce risque, abordé en théorie dans le mémoire, s'est réalisé plusieurs fois.
- **Le financement quadratique** : l'argent va aux projets soutenus par beaucoup de gens, pas par quelques gros donateurs.
- **Le vote par conviction** : le poids d'une voix grandit avec le temps pendant lequel on la maintient.
- **Les chambres séparées** : une chambre qui vote avec des tokens, une autre composée de personnes identifiées, chacune avec ses sujets.
- **Le retour de la futarchie** : des DAO qui décident par marchés de prédiction.
- **Les agents IA** comme participants ou délégués, exactement ce que ce projet simule.

### 4.4 Ce qui existe déjà en simulation

**Des outils.**

- **Mesa** : la bibliothèque Python de référence pour les simulations à base d'agents. Elle fournit les briques de base (modèle, agents, ordonnancement), la collecte de données et l'exécution en lots.
- **cadCAD** : outil de simulation né dans l'écosystème crypto, pour concevoir des mécanismes économiques et de gouvernance. Il pratique les tirages répétés (Monte-Carlo), les tests A/B et le balayage de paramètres : les modes duel et série du simulateur (§7.3) correspondent à des pratiques établies.

**Des recherches.**

- Des modèles à base d'agents testent déjà le vote quadratique, les jetons de réputation ou la délégation sur des DAO simulées. La démarche est reconnue, et ces modèles serviront de points de comparaison.
- Une étude récente fait voter un agent IA sur plus de 3 000 propositions réelles de DAO et compare ses choix à ceux des humains. C'est une référence directe pour la V8.
- Des études empiriques fournissent les chiffres qui servent à valider le modèle (§10.2).

### 4.5 Comment le mémoire sert le projet

Le mémoire s'arrête là où le simulateur commence.

- **Le tableau 4 devient l'espace des paramètres du jeu.** Chaque « principe clé » est un réglage ; chaque « réponse possible » est une option de ce réglage. Le simulateur est une boîte de Zwicky jouable.
- **L'étape 5 de l'analyse morphologique**, impossible en 2019 faute de données historiques, devient faisable : relier une configuration à un résultat. Le mode série produit exactement ces données.
- **L'évaluation de cohérence croisée** (certaines options sont incompatibles entre elles) devient une règle du jeu : le simulateur refuse les combinaisons incohérentes, ou montre ce qui se passe quand on les force.
- **La section sur les incitations** fournit la base de la question de l'initiative (§6) : récompenser les auteurs de propositions adoptées, demander une caution, faire perdre de la réputation aux inactifs.
- **La critique de Zamfir** donne la dernière brique : une DAO qui vote sur ses propres règles en cours de partie.

---

# Partie 3 — Le simulateur

## 5. Le principe : un laboratoire de constitutions

Je ne joue pas un membre de la DAO. **Je joue le rédacteur de la constitution.**

Une partie suit toujours la même boucle :

1. **Régler** : je choisis les paramètres (quorum, majorité, répartition des tokens, profils des membres…).
2. **Simuler** : les membres proposent, votent, la DAO construit ou échoue.
3. **Analyser** : le simulateur produit un rapport qui explique ce qui s'est passé et pourquoi.
4. **Ajuster** : je modifie un paramètre et je relance.

Chaque version, dès la V1, permet cette boucle sans limite.

**Le simulateur sert à répondre à des questions** (§6). Mais il ne peut pas *prouver* ce qui motive les humains : il montre ce qui se passe *si* les gens se comportent d'une certaine façon. Chaque réponse est donc conditionnelle : « sous ces hypothèses, tel mécanisme produit tel effet ». C'est déjà beaucoup : c'est exactement ce que le mémoire ne pouvait pas tester.

## 6. Le registre des questions de recherche

Chaque version, à partir de la V1, part d'une question et se termine quand le simulateur permet d'y apporter des éléments de réponse. Les questions de départ viennent des critiques réelles adressées aux DAO et de mes propres interrogations.

| Question | Ce qu'il faut modéliser | Version |
|---|---|---|
| Comment le quorum change-t-il le déroulement d'une partie ? | Vote simple | V1 |
| Quel quorum maximise les chances de réussite, au-delà de la chance ? | Modes duel et série | V2 |
| Les quartiers les plus touchés par un événement obtiennent-ils une réponse ? | Événements, besoins, propositions motivées | V3 |
| **Qu'est-ce qui pousse les membres à prendre des initiatives ?** (question posée avec Alex) | Proposer devient une décision avec un coût et une récompense ; adaptation des membres | V4 |
| Une DAO transparente décide-t-elle mieux ? | Niveaux d'information (§9) | V5 |
| La délégation recrée-t-elle des élus de fait ? | Délégation, coalitions | V6 |
| Le vote par token mène-t-il forcément à la ploutocratie ? | Token, réputation, une personne une voix | V6 |
| Une minorité organisée peut-elle capturer la caisse ? | Attaques, seuils, délai de sécurité | V7 |
| Les membres qui ne votent jamais profitent-ils du travail des autres ? | Passager clandestin, récompenses | V4 |
| Les contributeurs actifs s'épuisent-ils ? | Fatigue, charge de travail par membre, surcharge des délégués | V6 |
| Une DAO peut-elle réformer ses propres règles sans se bloquer ? | Méta-gouvernance | V9 |

Ce registre grandit au fil du projet. Une recherche documentaire sur les critiques des DAO viendra le compléter.

## 7. Ce que chaque simulation produit

### 7.1 Rejouer à volonté

- Lancer autant de parties que je veux.
- Modifier n'importe quel paramètre entre deux parties.
- **Réinitialiser** tous les paramètres à leurs valeurs par défaut en une commande.
- **Sauvegarder** une configuration sous un nom (« quorum-bas », « baleine-60 ») pour la recharger plus tard.

### 7.2 Le rapport de partie (dès la V1)

Chaque partie produit un rapport, sous forme de page HTML, en quatre parties :

1. **Résumé** : victoire ou défaite, en combien de tours, et la cause principale.
2. **Journal** : chaque tour en une ligne (proposition, résultat du vote, trésorerie).
3. **Graphiques** :
   - trésorerie au fil des tours ;
   - taux de participation à chaque vote ;
   - propositions adoptées, rejetées, et rejetées faute de quorum ;
   - poids de chaque profil de membres dans les décisions.
4. **Leçons** : des constats calculés à partir des chiffres, par exemple :
   - « 7 propositions sur 12 ont échoué faute de quorum : la participation est le problème, pas le désaccord » ;
   - « les prudents ont bloqué 80 % des investissements supérieurs à 150 » ;
   - « aucun bâtiment construit avant le tour 9 : la DAO a perdu 270 en frais fixes avant d'investir ».

### 7.3 Comparer : les modes duel et série (dès la V2)

**Le problème.** Le hasard intervient dans chaque partie : qui propose quoi, comment votent les absentéistes, ce que rapporte le Marché. Une victoire ou une défaite peut donc venir des règles ou simplement de la chance. Les deux modes servent à séparer les deux.

**Le mode duel : isoler l'effet d'un changement.**
Exemple : je veux savoir si baisser le quorum de 40 % à 25 % aide la DAO. Le duel joue deux parties avec exactement les mêmes tirages au sort (mêmes propositions, dans le même ordre, mêmes votes au hasard). La seule différence est le quorum. Si l'une gagne et l'autre perd, c'est forcément le quorum qui a fait la différence.
Image : tester deux recettes avec les mêmes ingrédients.

**Le mode série : ne pas se fier à une seule partie.**
Une partie gagnée ne prouve pas grand-chose : les propositions sont peut-être tombées dans un ordre favorable. La série joue la même configuration 100 fois, avec des tirages différents à chaque fois. Résultat attendu : « avec un quorum de 25 %, la DAO gagne 68 fois sur 100 ; avec 40 %, 41 fois sur 100 ». On sait alors que c'est la règle qui compte, pas la chance.
Image : lancer un dé cent fois pour savoir s'il est pipé, plutôt qu'une seule fois.

**En résumé** : le duel explique *pourquoi* un changement agit, la série dit *s'il marche vraiment*. C'est la série qui transforme le jeu en outil d'analyse.

## 8. Le cadre : de la DAO abstraite à Metz

### 8.1 L'horizon

À terme, la DAO ne gère pas une ville imaginaire partie de rien, mais **Metz**.

Le scénario : un maire élu en 2026, sans nom ni étiquette politique, décide de confier une partie des décisions municipales à une DAO d'habitants. La DAO démarre avec la ville telle qu'elle est : ses quartiers, son budget, ses équipements, ses besoins. C'est une fiction assumée. En droit français, un conseil municipal ne peut pas déléguer ses décisions à une DAO, mais il peut s'engager à appliquer les votes des habitants, comme pour un budget participatif.

### 8.2 Ce que ça change par rapport à une DAO abstraite

- **On ne part pas de zéro** : il y a un existant à entretenir, pas seulement des choses à construire.
- **Le but n'est pas le profit** : la réussite se mesure au bien-être des habitants, quartier par quartier, avec un budget tenu.
- **Les membres ne sont pas égaux en intérêts** : un habitant de Borny et un habitant du Centre-Ville n'ont pas les mêmes priorités. Les conflits entre quartiers deviennent un enjeu de gouvernance.
- **Qui vote ?** Dans une ville, « 1 token = 1 voix » voudrait dire que les riches achètent la mairie. La question token / réputation / une personne une voix devient concrète.

### 8.3 Une montée en réalisme progressive

| Étape | Cadre | Ce qu'on ajoute | Versions |
|---|---|---|---|
| **A** | DAO abstraite | La mécanique de vote seule | V1–V2 |
| **B** | Petite ville fictive | 3 quartiers, un budget d'investissement, des événements, un indicateur de satisfaction par quartier | V3–V5 |
| **C** | Metz simplifiée | Les vrais quartiers (Centre-Ville, Sablon, Borny, Queuleu, Devant-les-Ponts…), les grands postes du budget (voirie, écoles, transports, culture, espaces verts), une population par quartier issue des données publiques | V6–V7 |
| **D** | Metz 2026 | Un état de départ construit à partir de données ouvertes réelles, des habitants pilotés par une IA, le scénario complet du maire | V8 et au-delà |

### 8.4 Des propositions ancrées dans la réalité

En V1 et V2, les propositions sont tirées au hasard. C'est une simplification volontaire, pour tester la mécanique de vote seule.

À partir de la V3, les propositions naissent d'un contexte :

1. **Un événement survient** : un orage abîme un pont, une subvention arrive, une usine ferme, une école déborde.
2. **Il crée un besoin**, localisé dans un ou plusieurs quartiers.
3. **Les membres concernés proposent une réponse**, selon leurs intérêts.
4. **La DAO vote**, et le besoin est satisfait ou non. S'il ne l'est pas, il s'aggrave.

À partir de la V4, proposer devient une décision du membre, avec un coût et une récompense.

### 8.5 L'unité de temps : un tour = un mois

- C'est une durée de vote réaliste : certaines DAO étudiées dans le mémoire, comme Bisq, votent sur un mois.
- Le budget municipal est annuel : une année = 12 tours.
- Un mandat municipal dure six ans : un mandat = 72 tours.
- En V1, 30 tours correspondent à deux ans et demi.

### 8.6 L'échelle : un échantillon représentatif

Metz compte plus de 100 000 habitants. Simuler chacun serait très lourd, et impossible avec des agents IA. À partir de l'étape C, les membres forment donc un **échantillon représentatif**, comme un sondage : par exemple 1 000 membres, chacun pesant une centaine d'habitants, répartis selon la population et le profil réels des quartiers.

## 9. L'information, objet d'étude central

Le mémoire reprend une promesse courante : une DAO serait totalement transparente, donc sans asymétrie d'information. C'est une affirmation à mettre à l'épreuve. Des données publiques ne font pas des membres informés : s'informer prend du temps, et beaucoup choisissent de ne pas le faire. C'est l'*ignorance rationnelle*, déjà citée dans le mémoire.

L'information devient donc un ensemble de paramètres réglables, ajoutés progressivement et rapprochés autant que possible de la réalité :

- **Ce que chaque membre voit** : l'état de la caisse, les besoins des quartiers, les conséquences probables d'une proposition.
- **Le coût pour s'informer** : un membre peut voter sans s'informer, ou investir du temps pour mieux comprendre.
- **La visibilité des votes en cours** : voir comment votent les autres crée du suivisme.
- **La qualité de l'information** : erreurs, rumeurs, propositions présentées de façon trompeuse.

Jusqu'à la V4, l'information est parfaite : tout le monde sait tout. C'est le point de référence à partir duquel on mesurera l'effet de chaque imperfection.

## 10. Le modèle : principes, validation, limites

### 10.1 Principes techniques

**1. Tous les membres parlent la même langue.**
Le simulateur pose à chaque membre une seule question : « voici la proposition et l'état de la DAO, que votes-tu ? ». Aujourd'hui une règle de trois lignes répond ; plus tard, peut-être une IA. Le reste du simulateur ne fait pas la différence.

**2. Le hasard est reproductible.**
Une *graine* fixe tous les tirages au sort. Même graine = même partie. Indispensable pour tester le code et pour comparer deux constitutions.

**3. La simulation et le rapport sont séparés.**
La simulation produit des données (ce qui s'est passé à chaque tour). Le rapport lit ces données et les met en forme. On peut ainsi améliorer les graphiques sans toucher aux règles, et inversement.

**4. Les paramètres vivent dans un fichier.**
Un fichier de configuration lisible contient tous les réglages. Réinitialiser, c'est recharger le fichier par défaut ; sauvegarder, c'est en écrire une copie.

**5. Le modèle est décrit selon le protocole ODD.**
ODD (*Overview, Design concepts, Details*) est la méthode standard en recherche pour décrire une simulation à base d'agents. Un fichier `docs/odd.md`, tenu à jour à chaque version, répond à ses questions : à quoi sert le modèle, quelles entités, dans quel ordre se passent les choses, ce qui est aléatoire, ce que les agents savent, s'ils apprennent, comment ils interagissent. N'importe quel chercheur peut ainsi comprendre et critiquer le modèle.

**6. Python simple d'abord, Mesa peut-être ensuite.**
Les V1 et V2 sont écrites en Python simple, sans bibliothèque de simulation, pour comprendre la mécanique de l'intérieur. Le code sépare dès le départ un « modèle » et des « agents », comme Mesa. À la V3, je décide de continuer seul ou de migrer vers Mesa : une vraie décision *build or buy*, et une leçon de PO en soi.

### 10.2 Validation : les faits que le modèle doit reproduire

Un modèle n'est crédible que s'il reproduit, avec des réglages réalistes, ce qu'on observe dans les vraies DAO. Les études empiriques donnent des repères :

- **Une participation faible** : en moyenne autour de 6 % des détenteurs de tokens votent sur une proposition, contre 70 à 80 % des actionnaires dans les grandes entreprises cotées.
- **Un pouvoir concentré** : les 10 % de votants les plus puissants détiennent environ les trois quarts du pouvoir de vote exercé.
- **Une concentration qui augmente** à mesure que les DAO grandissent.
- **Des écarts importants entre DAO** : certaines atteignent plus de 60 % de participation en pouvoir de vote. La faible participation n'est pas une fatalité, ce qui en fait une bonne question de recherche.

Règle : à partir de la V4, les profils de membres doivent pouvoir reproduire ces ordres de grandeur. Si le modèle ne sait pas recréer une DAO réaliste, ses leçons sur une DAO « idéale » ne valent rien.

### 10.3 Ce qui manque encore au modèle

- **L'adaptation** : les membres changent-ils de comportement avec le temps ? Un membre dont les propositions sont toujours rejetées se décourage-t-il ? Un absentéiste se mobilise-t-il quand son quartier est touché ? Central pour la question de l'initiative. Arrivée prévue : V4.
- **Les interactions** : pour l'instant, chacun vote seul. Coalitions, influence et persuasion n'existent pas. Arrivée prévue : V6, avec la délégation.
- **La culture et la délibération** : ce que le mémoire appelle la gouvernance off-chain. Elles se simulent mal ; c'est une limite à rappeler dans chaque rapport.

## 11. Règles de la V1 — la « Minimum Viable DAO »

Tout ce qui n'est pas dans cette section n'existe pas encore. C'est volontaire. La V1 correspond à l'étape A : une DAO abstraite, sans ville.

### 11.1 Situation de départ

- **10 membres**, chacun avec **100 tokens** (1 000 tokens au total).
- **Trésorerie : 500 crédits.**
- **Frais fixes : 30 crédits par tour.** Si on ne construit rien, la caisse se vide lentement.

### 11.2 Ce qu'on peut construire

| Bâtiment | Coût | Rapporte par tour |
|---|---|---|
| Ferme | 100 | 20 |
| Atelier | 200 | 45 |
| Marché | 150 | 0 ou 80, au hasard (pari risqué) |

### 11.3 Un tour de jeu, étape par étape

1. **Proposition** : un membre tiré au hasard propose de construire un bâtiment tiré au hasard.
2. **Vote** : chaque membre vote *oui*, *non*, ou ne vote pas.
3. **Dépouillement** :
   - le quorum est-il atteint ? (défaut : 40 % des tokens ont voté) ;
   - si oui, les « oui » dépassent-ils la majorité ? (défaut : plus de 50 % des votes exprimés).
4. **Exécution** : si la proposition est adoptée et que la trésorerie suffit, le bâtiment est construit et payé.
5. **Revenus et frais** : chaque bâtiment rapporte, puis on retire les frais fixes.
6. **Vérification** : victoire, défaite, ou tour suivant.

### 11.4 Les membres : trois profils

Les membres ne sont pas des IA. Ce sont des règles de décision très simples.

| Profil | Nombre | Comment il vote |
|---|---|---|
| **Prudent** | 4 | *Oui* si le coût est inférieur ou égal à 30 % de la trésorerie, sinon *non* |
| **Dépensier** | 3 | Vote toujours *oui* |
| **Absentéiste** | 3 | Ne vote qu'une fois sur trois ; quand il vote, c'est au hasard |

### 11.5 Victoire et défaite

- **Victoire** : la trésorerie atteint **2 000 crédits** à la fin d'un tour, au plus tard à la fin du tour 30.
- **Défaite** : la trésorerie passe sous zéro, ou le tour 30 se termine sans victoire.

Ces chiffres sont des valeurs de départ. Ils seront ajustés une fois la V1 codée, pour que la partie ne soit ni gagnée ni perdue d'avance.

### 11.6 Exemple : le tour 1 déroulé

- Trésorerie : 500. Proposition : **construire un Atelier (200)**.
- Les **4 prudents** calculent : 200 / 500 = 40 %, plus que 30 %. Ils votent *non* → **400 tokens contre**.
- Les **3 dépensiers** votent *oui* → **300 tokens pour**.
- Parmi les **3 absentéistes**, un seul vote, et il tire *oui* → **100 tokens pour**.
- Participation : 800 / 1 000 = 80 %. **Quorum atteint.**
- Résultat : 400 *oui*, 400 *non*, soit exactement 50 %. Il faut *plus* de 50 %. **Rejetée.**
- Fin de tour : aucun revenu, 30 de frais. **Trésorerie : 470.**

Premier enseignement : avec ces règles, les prudents bloquent les gros investissements en début de partie. C'est le genre de constat que le rapport doit faire ressortir tout seul.

### 11.7 Ce que je peux régler

- Le quorum et la majorité.
- Le nombre de membres de chaque profil.
- La répartition des tokens (égale, ou concentrée sur quelques membres).
- La graine aléatoire.

### 11.8 Ce que la V1 ne fait pas (exprès)

Pas d'interface de jeu graphique, pas de blockchain, pas d'IA, pas de délégation, pas de ville, pas d'événements, pas de modes duel et série, information parfaite. Le simulateur se lance dans un terminal et produit son rapport sous forme de page HTML.

---

# Partie 4 — La démarche

## 12. Apprendre : du cadrage au code

### 12.1 Ce document n'est pas une spec

Ce document fixe la vision. Il est trop large pour guider directement un agent qui code. Avant chaque version, on en dérive trois documents :

| Document | Rôle | Qui le lit |
|---|---|---|
| `CLAUDE.md` | Court. Règles du projet, conventions, façon de travailler | Claude, à chaque session |
| Spec de version | Précise. Règles exactes, entrées et sorties, cas de test attendus | Moi et Claude, pour la version en cours |
| Backlog | Les tâches découpées, dans l'ordre | Moi, pour piloter |

Cette chaîne vision → spec → backlog → instructions à l'agent est le cœur du métier de PO avec des agents. C'est la première leçon.

### 12.2 Les leçons écrites

Chaque étape s'accompagne d'une leçon, rangée dans le dossier `lecons/` du dépôt. Toutes suivent le même format :

1. **Ce qu'on va faire** : la brique à ajouter, en une phrase.
2. **Le concept** : expliqué pour un débutant.
3. **Pourquoi maintenant** : ce qui rend cette étape nécessaire à ce stade.
4. **L'outil Claude Code** : la fonctionnalité utilisée (mode plan, subagent, hook, skill…) et son fonctionnement.
5. **L'exercice** : ce que je fais concrètement, pas à pas.
6. **Ce que ça change pour un PO** : la pratique professionnelle qui en découle.
7. **Les pièges** : les erreurs classiques.

Les leçons, le journal de bord (§14) et les publications forment ensemble la trace de la méthode.

### 12.3 Le coaching de prompts

Bien formuler une demande à un agent est le geste de base du PO avec des agents. Mes prompts sont donc challengés, en conversation comme dans Claude Code.

**Quand** : sur les prompts qui lancent du travail (une spec, une tâche, une décision), pas sur les questions rapides.

**La progression** : d'abord des **modèles de prompts commentés**, que je relis et ajuste. L'écriture autonome viendra progressivement, quand je me sentirai à l'aise ; le coaching ci-dessous s'applique alors à mes propres prompts.

**Le format du retour** :

1. **Ce qui marche** dans le prompt.
2. **Ce qui manque**, au regard de la grille ci-dessous.
3. **Une structure proposée**, sans réécrire le prompt à ma place.
4. **« À toi de recommencer »** : je réécris, et je reçois un nouveau retour si besoin.

**La grille d'un bon prompt** :

| Élément | Question à se poser |
|---|---|
| Contexte | Qu'est-ce que l'agent doit savoir pour comprendre la situation ? |
| Objectif | Quel résultat précis j'attends ? |
| Contraintes | Qu'est-ce qui est interdit, imposé, limité ? |
| Format de sortie | Sous quelle forme je veux la réponse ? |
| Critère de fin | Comment saura-t-on que c'est terminé et réussi ? |
| Exemples | Ai-je un exemple de ce que je veux, ou de ce que je ne veux pas ? |

**Dans Claude Code**, une règle du `CLAUDE.md` demande à Claude de faire ce retour avant d'exécuter une tâche importante.

**Dans le journal de bord**, je garde les paires « prompt avant / prompt après » les plus instructives : elles montrent la progression.

## 13. Feuille de route

Chaque version répond à une question du registre (§6), avance dans le cadre de la ville (§8.3), et fait apprendre une compétence Claude Code.

| Version | Étape | Brique | Compétence Claude Code |
|---|---|---|---|
| **V0** | — | Installation : terminal, git, Python, Claude Code ; premier petit programme | Premiers échanges avec Claude, lire du code |
| **V1** | A | Vote simple pondéré, quorum, majorité, rapport de partie | `CLAUDE.md`, mode plan, tests, git |
| **V2** | A | Modes duel et série, rapports comparatifs | Écrire les tests avant le code, subagent de relecture |
| **V3** | B | Quartiers, événements, besoins, propositions motivées ; décision Python simple ou Mesa | Hooks (tests lancés automatiquement) |
| **V4** | B | Proposer devient une décision (coût, récompense, caution) ; adaptation des membres ; validation sur les chiffres réels | Skills et commandes personnalisées |
| **V5** | B | Niveaux d'information | Sessions parallèles, worktrees |
| **V6** | C | Échantillon représentatif de Metz ; délégation, coalitions et influence ; qui vote : token, réputation ou une personne une voix | MCP, données ouvertes |
| **V7** | C | Seuils différenciés, délai de sécurité, attaques, protection des minorités | Subagent « red team » qui cherche les failles |
| **V8** | D | Habitants pilotés par une IA | API Claude, Agent SDK, maîtrise des coûts |
| **V9** | D | La DAO vote sur ses propres règles | Orchestration multi-agents |
| **V10** | D | Interface visuelle de la ville | Frontend, tests dans le navigateur |

**Abonnement** : Pro suffit jusqu'à la V4 environ. Max se justifie quand le travail en parallèle et les agents deviennent le quotidien (V5 et au-delà).

## 14. Organisation

- **Rythme** : 4 à 6 heures par semaine. Ordre de grandeur : deux semaines pour la V0, trois à quatre pour la V1.
- **Langue** : tout le projet est en français (documentation, commentaires du code, leçons, publications).
- **Dépôt public dès le départ**, sur GitHub, organisé ainsi :

| Dossier ou fichier | Contenu |
|---|---|
| `CLAUDE.md` | Les instructions pour Claude |
| `docs/` | Ce document de cadrage, les specs de version, `odd.md` |
| `lecons/` | Les leçons écrites |
| `journal/` | Le journal de bord PO (privé : exclu de git, jamais publié) |
| `config/` | Les fichiers de paramètres (défaut et sauvegardes) |
| `src/` et `tests/` | Le code et ses tests |

- **Licences** : MIT pour le code (chacun peut le réutiliser librement en citant l'auteur) ; Creative Commons BY 4.0 pour les textes (leçons, journal, articles).
- **Une publication par version**, en trois parties : ce que j'ai construit, ce que la simulation m'a appris sur les DAO, ce que j'ai appris sur le travail avec des agents.
- **Le journal de bord PO**, privé : il reste sur mon Mac, exclu de git par le `.gitignore`. À chaque session : l'objectif, comment j'ai briefé Claude, ce qui a marché ou non, les décisions prises. C'est la matière première des publications, qui en reprennent ce que je choisis de partager, et des futurs entretiens.
- **Contributions extérieures** : ouvertes plus tard, une fois les tests et un guide de contribution en place. Piste : faire décider l'évolution du projet par ses contributeurs selon les règles de gouvernance testées dans le simulateur.

## 15. Règles de travail

1. **Une brique à la fois.** On n'ajoute rien tant que la version en cours n'est pas testée.
2. **Je comprends le code avant de valider.** Si je ne comprends pas une modification, je demande une explication avant de l'accepter.
3. **J'écris la spec, Claude écrit le code.** Chaque version commence par une courte description rédigée par moi.
4. **Chaque version part d'une question du registre** (à partir de la V1), et se termine quand le simulateur permet d'y apporter des éléments de réponse.
5. **Une question de modélisation ne bloque jamais plus d'une session.** Au-delà, on prend l'option la plus simple et on la note comme hypothèse à revoir.
6. **Chaque version se termine par un rituel de clôture** :
   - une rétrospective courte dans le journal : ce qui a marché, ce qui n'a pas marché, ce que j'ai appris sur les DAO et sur le travail avec des agents ;
   - une relecture de ce document de cadrage, mis à jour si la réalité du projet s'en est écartée ;
   - la publication de l'article de la version.
7. **Aucun secret dans le dépôt.** Clés d'API, mots de passe et jetons d'accès ne sont jamais envoyés sur GitHub. Un fichier `.gitignore` les exclut dès la V0.

## 16. Risques et limites

| Risque | Parade |
|---|---|
| **Le simulateur confirme mes propres hypothèses** : le comportement des membres est inventé, donc les leçons reflètent mes choix, pas la réalité | Ancrer les profils dans des données réelles (§10.2) ; formuler chaque leçon au conditionnel : « si les membres se comportent ainsi, alors… » |
| **Un modèle non crédible** | Validation sur les chiffres réels avant toute leçon sur une DAO « idéale » |
| **Les agents IA cassent la reproductibilité et coûtent cher en série** | Décider avant la V8 : les agents IA explorent des comportements et servent à calibrer les profils à règles, qui restent ceux du mode série |
| **La condition de réussite décide du résultat** | Afficher plusieurs indicateurs (bien-être moyen, équité entre quartiers, budget tenu) et montrer qu'une constitution peut réussir sur l'un et échouer sur l'autre |
| **Conflit entre les objectifs** : bloqué sur la modélisation sans coder, ou l'inverse | Règle de travail n° 5 ; ordre des arbitrages (§2.3) |
| **Démarrer sans aucune base en code** | V0 dédiée aux bases ; règle « je comprends avant de valider » ; leçons écrites pour débutant |
| **Outils avancés artificiels sur un petit code** | L'accepter : on apprend le geste maintenant, sa valeur apparaîtra quand le code grossira |
| **Réinventer ce qui existe** | Veille tenue à jour (§4.4) ; décision Mesa à la V3 ; comparaison avec les modèles publiés |
| **Projet solo, sans retour extérieur** | Rythme fixe, dépôt public, une publication par version |
| **Ce n'est pas un jeu mais un laboratoire** | L'assumer ; ajouter plus tard des décisions du joueur en cours de partie si l'envie vient |
| **La culture et la délibération ne se simulent pas** | L'écrire comme limite dans chaque rapport, pour ne pas surinterpréter |
| **Metz réelle : terrain politique** | Maire sans nom ni étiquette ; choix de modélisation documentés et publics |

## 17. Décisions et questions ouvertes

### 17.1 Décisions prises

| Sujet | Décision |
|---|---|
| Langage | Python |
| Moteur de simulation | Python simple pour V1–V2 ; Mesa ou non, décidé à la V3 |
| Environnement | Mac, Claude Code en local |
| Unité de temps | Un tour = un mois |
| Échelle de Metz | Échantillon représentatif pondéré (environ 1 000 membres) |
| Langue | Français |
| Visibilité | Dépôt public dès le départ ; journal de bord privé, exclu de git |
| Licences | MIT pour le code, CC BY 4.0 pour les textes |
| Rythme | 4 à 6 heures par semaine |
| Ordre des arbitrages | Apprentissage PO > réalisme > périmètre > vitesse |
| Nom du projet | DAO Simulator (provisoire) |
| Coaching de prompts | Modèles commentés d'abord ; écriture autonome progressive, avec retours sur mes prompts |

### 17.2 Questions ouvertes

- **Où publier les articles** : le dépôt GitHub seul, un blog, LinkedIn ? À trancher à la fin de la V1.

## 18. Critère de réussite de la V1

La V1 est terminée quand :

- [ ] une partie complète tourne, du tour 1 à la victoire ou la défaite ;
- [ ] la même graine donne toujours la même partie ;
- [ ] les règles de vote sont couvertes par des tests ;
- [ ] je peux modifier un paramètre, relancer, et réinitialiser les paramètres ;
- [ ] chaque partie produit un rapport HTML avec résumé, journal, graphiques et au moins trois leçons ;
- [ ] je sais expliquer chaque fichier du projet ;
- [ ] le journal de bord couvre chaque session ;
- [ ] l'article de la V1 est publié.

---

# Sources

- Bouard P., *Morphological Analysis of a viable Decentralized Autonomous Organization*, mémoire de master, ESCP Europe, 2019.
- Cong et al., *Centralized Governance in Decentralized Organizations* — participation et concentration du vote : https://afajof.org/management/viewp.php?n=157500
- *Democracy for DAOs* (écosystème Internet Computer) — DAO à forte participation : https://arxiv.org/html/2507.20234
- *DAO-AI: Evaluating Collective Decision-Making through Agentic AI in Decentralized Governance* : https://arxiv.org/abs/2510.21117
- *Quadratic Voting and Reputation Tokens in Physical DAOs: An Agent-Based Model* : https://journals.jps.jp/doi/abs/10.7566/JPSCP.44.011008
- *Navigating the Research Landscape of DAOs* — outils de simulation, cadCAD : https://arxiv.org/pdf/2312.17197
- Mesa : https://github.com/projectmesa/mesa
