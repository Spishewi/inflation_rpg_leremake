# RAPPORT PROJET POO "Inflation RPG Leremake"

***Thomas BIORET - Aurèle AUMONT--VESNIER***

## Avant propos
Ayant déjà de l'experience dans les jeux graphiques avec pygame,
nous avons décidé, bien que celà ne rentre que très peut dans la note,
de créer un jeu graphique. Nous avons bien sûr tout de même essayé de coller au mieux aux contraintes. Sachant que nous savons que vous connaissez déjà le vocabulaire, nous ne nous attarderons pas sur tout les mots lié au jeu vidéo, et nous autorisons les anglissismes connu. (equipement, stats, level-up...)

## Description du projet
Notre jeu s'inspire fortement du jeu [inflation RPG](https://play.google.com/store/apps/details?id=air.infurerpgkuesuto&hl=fr).

Le jeu s'articule autour d'un gameplay roguelite. Nous sommes laché à chaque partie dans une grotte, et le but est d'aller le plus loin possible et de level-up en un nombre donné de combat. A la fin de la partie, une récompense proportionnelle au niveau obtenu sera donné, permettant d'améliorer de l'equipement en vue d'une autre partie.

Le jeu contient donc une gestion de niveau et de stats remise à zéro à chaque partie, et d'une gestion de l'équipement, elle, sauvegardé entre les parties.

Les combats se lancent aléatoirement en fonction de la barre de combat (en bas de l'écran), et se font automatiquement suivant la zone de niveau dans laquelle le joueur se trouve au moment où le combat se lance. L'issue du combat est donc déterminé suivant la zone où le joueur se trouve et sa chance. Il est du devoir du joueur d'aller dans une zone assez haut level pour pouvoir monter rapidement en niveau, tout en faisant attention à ne pas voir trop grand.

## dépendances

- python 3.6+
  - [pygame](https://github.com/pygame/pygame) 2.1+
  - [pytmx](https://github.com/bitcraft/pytmx) 3.31
  
### Python

**ATTENTION** : Nous utilisons des fonctionnalités récente de python, comme les "type-hint". Ces fonctionnalités ne fonctionne que sur les versions de python ultérieurs à python 3.9+.
Une méthode très simple pour permettre d'utiliser ces annotations dans de plus anciennes version de python (comme celles du lycée) est d'ajouter cette ligne en haut de chaques fichiers
```py
from __future__ import annotations
```
Normalement nous avons fait attention à mettre celà partout, mais nous prévenons quand même, car nous ne savons pas si nous aurons le temps de tester le jeu sur les ordinateurs du lycée.

### Pygame
Ce module permet l'affichage graphique du jeu. Il est donc indispensable.

**ATTENTION** : pygame n'est pas à ce jour disponible pour python 3.11 (la dernière version de python). De ce fait, notre programme n'est pas non plus compatible avec cette dernière version.

### Pytmx
Ce module nous permet de charger des fichiers de map pour notre jeu. Sans ce module, nous ne pouvons pas charger de map, ou très difficilement. (convertissant à la main des fichiers de map en csv, puis en les lisant tel quel). Il permet concrêtement de *parser* les fichiers **.tmx**, fichier de carte créé par l'éditeur de carte renommé [Tiled](https://www.mapeditor.org/). Celà permet ensuite à notre programme de jouer avec l'objet `TiledMap`, afin d'afficher la carte, connaitre l'emplacement des zones, des collisions...


## Installation

### dépendances
Nous partons du principe que votre environnement admet un python correctement installé, dans une des versions compatibles (3.6 à 3.10), et que les variables d'environnement sont correctement initialisé (c'est le cas au lycée).

Pour installer les dépendances il suffit d'effectuer les commandes suivantes.
```powershell
# installer pygame et/ou le mettre à jour
python -m pip install pygame --upgrade

# installer pytmx
python -m install pytmx
```

### lancement
Pour lancer le jeu depuis le terminal, il faut lancer le fichier `main.py`, situé dans le dossier `src/`. pour celà, effectuez les commandes suivantes :
```powershell
# se déplacer dans le dossier "src/" du projet
cd "[le/chemin/vers/le/dossier/du/projet]/src"

# lancer le jeu
python main.py
```

## Première partie de jeu

Lorem consequat velit est qui qui officia. Laborum tempor ullamco consectetur adipisicing nostrud aute laboris labore et nulla. Veniam incididunt consequat quis est enim ut nulla. Incididunt enim consequat elit occaecat quis duis enim anim velit commodo.

Sunt excepteur eiusmod velit irure consequat. Qui veniam amet cupidatat cupidatat consequat duis in cillum proident aliqua magna irure eu. Enim pariatur dolore anim veniam incididunt mollit aliqua consectetur labore culpa laboris et duis. Officia dolore incididunt elit do do ipsum ullamco nisi et.

Deserunt laborum ut nulla ullamco minim mollit velit magna et laboris esse est. Veniam laboris non cillum fugiat Lorem. Et quis sit commodo ullamco ad velit ea occaecat pariatur officia. Laborum eu minim proident fugiat cillum duis aute laboris sit cillum. Cillum sunt et quis aute Lorem nisi aliqua.

Aute voluptate nostrud consequat esse est proident id incididunt sint cillum duis fugiat aliqua irure. Id mollit culpa non occaecat mollit Lorem ad laboris in enim id excepteur duis sit. Ullamco ex reprehenderit voluptate ut elit eu pariatur.

Commodo dolore incididunt non duis excepteur magna pariatur. Minim deserunt nostrud aliqua cupidatat consectetur ex elit ea nisi sit. Sint excepteur labore id laboris minim nulla ad irure ea anim irure consequat veniam in. Nostrud ea proident consectetur ullamco eu est consequat. Nisi fugiat elit reprehenderit dolore nisi in tempor excepteur minim nulla deserunt ut cupidatat.

## Fonctionnalités manquantes

Irure labore qui irure mollit est sint dolor do velit enim adipisicing ea exercitation do. Qui ullamco reprehenderit ullamco excepteur est esse esse nisi. Lorem nulla exercitation dolor occaecat cupidatat voluptate adipisicing ut minim ut sunt occaecat reprehenderit proident. Lorem Lorem enim et non nulla labore elit nulla officia anim magna. Nisi enim est do consequat commodo fugiat veniam quis proident culpa quis exercitation fugiat duis. Proident commodo eu sunt labore id elit. Irure Lorem amet culpa pariatur cillum.

Tempor sit nulla consectetur minim dolore eu do duis do occaecat dolore non elit. Eiusmod cupidatat Lorem ex magna ut ad esse adipisicing aute proident. Sit laboris aliqua anim Lorem do. Tempor est labore mollit id id aliquip cillum nostrud cillum proident. Sunt fugiat ut commodo duis do labore adipisicing ex duis. Veniam aliquip anim dolore nostrud quis consectetur nisi aliqua id sunt occaecat.

Commodo sit occaecat qui consectetur ullamco labore. Ex reprehenderit dolore sint anim ut minim pariatur quis ad ullamco sunt enim aliqua irure. Qui dolor id do veniam ad proident consectetur tempor culpa ad magna elit. Sit quis amet magna aliquip exercitation labore culpa irure sint. Incididunt ut adipisicing id laboris minim. Eu ex eu dolore laboris nisi.

## Répartition du travail

Nous avons essayé de nous répartir au mieux le travail, bien que travailler pendant les vacances de noël s'est révélé beaucoup plus dûr que prévu.
Thomas, qui est meilleur sur tout ce qui est graphique s'est occupé des menus et de la carte.
Moi (c'est Aurèle qui écrit), je me suis occupé de tout ce qui est moteur de jeu (système de combat, gestion interne de la map, système de sauvegarde...).

Enfin nous avons travaillé ensemble sur le système d'équipement (car très lié à l'interface), ainsi que au système de stats en général. Afin d'équilibrer au mieux.

On peut regarder sur le github les participations de chacun pour plus de précision. (Si ce n'est pas public, je peut fournir les graphiques).

les fichiers `map_manager.py` et `camera_view.py` sont hérité de notre projet perso, mais très fortement modifiés. Tout les autres sont originaire directement du projet. (je ne sais en ce moment pas encore si nous utilisons votre fichier `filable.py`)