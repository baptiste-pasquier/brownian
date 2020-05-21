# brownian
<img src="./img/icon.png" alt="Icon" height="100"/> 
Modélisation d'un mouvement brownien

## Table des matières
* [A. Informations générales](#a-informations-générales)
* [B. Modélisations](#b-modélisations)
  - [Simulation de type 1](#simulation-de-type-1)
  - [Simulation de type 1.1](#simulation-de-type-11)
  - [Simulation de type 2](#simulation-de-type-2)
  - [Simulation de type 3](#simulation-de-type-3)
  - [Mesures](#mesures)
* [C. Installation](#c-installation)
* [D. Exemples](#d-exemples)
* [E. Utilisation](#e-utilisation)
* [F. Fonctionnalités](#f-fonctionnalités)


## A. Informations générales

Ce projet fournit différentes modélisations d'un mouvement brownien.

## B. Modélisations

Dans les différents modèles, nous suivons le mouvement d'une grosse particule dans un environnement constitué de nombreuses petites particules aléatoires.

### Simulation de type 1

**Utilisation de plusieurs petits environnements définis à chaque collision.**

<img src="./img/simulation1.gif" alt="Simulation de type 1" height="300"/> 

#### Algorithme 
Date t : Génération d’un environnement aléatoire centré autour de la grosse particule (de rayon h(v+V)). 

* Cas 1 : si aucune collision pendant la durée h, on fait avancer la grosse particule jusqu’à t + h, puis on régénère un nouvel environnement à cette position et au temps t + h

* Cas 2 : si une collision existe entre t et t+h (donc à l’intérieur du disque), on définit Δt la durée avant la première collision. On fait avancer la grosse particule jusqu’à la collision, puis on définit un nouvel environnement à cette position et au temps t + Δt. On change aléatoirement l’angle de la vitesse de la grosse particule.

#### Caractéristiques du modèle
1. Non prise en compte des collisions des petites particules
2. Environnement ouvert (sans rebond des petites particules), pas de génération de petite particule lorsqu’une petite particule sort de l’environnement
3. Plusieurs environnements

### Simulation de type 1.1

**Amélioration de la simulation de type 1.1.**
**Utilisation de plusieurs petits environnements définis à chaque collision.**

<img src="./img/simulation1_1.gif" alt="Simulation de type 1" height="300"/> 

Le temps est découpé en intervalles égaux de durée h, appelés étapes. On note nb_étapes le nombre total d’étapes et on numérote ces étapes par des entiers de 0 à nb_étapes.

#### Algorithme
Au début de l’étape e on génère une distribution aléatoire de petites particules dans un disque de rayon R=h*(v+V) où v est la vitesse des petites particules et V la vitesse de la grosse (en norme).
Si une collision se produit dans le disque, on amène la grosse particule au point d’impact, on change aléatoirement la direction de son vecteur vitesse, et on génère un nouvel environnement de petites particules dans un disque autour de la grosse et de rayon R-V*Δt, où Δt est le temps écoulé depuis le début de l’étape.
On réitère l’opération en détectant chaque fois les collision dans des disques de plus en plus petits (Δt est incrémenté à chaque collisions : notant t1, …, tn les instants des collisions durant l’étape e, on a Δt = t1 + … + tn ; ainsi Δt appartient toujours à [0,h]).
Lorsqu’il n’y a plus de collision détectée dans le dernier disque, on finit de faire avancer notre particule en ligne droite (pendant donc une durée de h - Δt), et on passe à l’étape e+1.

Cette méthode, bien que d'apparence moins naturelle, offre une réduction des coûts importante.
Le temps d'execution est dans la plupart des cas divisé par 2 ou 3 par rapport au modèle 1.

#### Caractéristiques du modèle : 
1. Non prise en compte des collisions des petites particules
2. Environnement ouvert (sans rebond des petites particules), pas de génération de petite particule lorsqu’une petite particule sort de l’environnement
3. Plusieurs environnements


### Simulation de type 2

**Utilisation d'un grand environnement unique.**

<img src="./img/simulation2.gif" alt="Simulation de type 2" height="300"/>

#### Algorithme 

On génère un unique et grand environnement aléatoire carré (de côté 2\*dim) centré autour de la grosse particule. 

A la première grosse collision possible à la date t + Δt, on fait avancer toutes les petites particules et la grosse particule pendant Δt. On change aléatoirement l’angle de la vitesse de la grosse particule et de la petite particule en collision. Si un petite particule se trouve hors de l’environnement (carré) on la supprime et on redéfinit une petite particule aléatoirement dans l’environnement.

#### Caractéristiques du modèle
1. Non prise en compte des collisions des petites particules
2. Environnement ouvert (sans rebond des petites particules), génération d’une petite particule aléatoire à chaque sortie d’une petite particule (pour avoir une densité constante)
3. Unique environnement


### Simulation de type 3

**Prise en compte des collisions des petites particules de l'environnement.**

<img src="./img/simulation3.gif" alt="Simulation de type 3" height="300"/>

#### Algorithme
Génération d’un unique et grand environnement aléatoire carré (de côté 2*dim) centré autour de la grosse particule. 

On détermine la première petite collision possible (date t + Δt1) et la première grosse collision possible (date t + Δt2).

* Si Δt1 < Δt2 (avec éventuellement Δt2 = ∞ si aucune grosse collision possible): on fait avancer toutes les particules pendant Δt1, puis on change aléatoirement l’angle des vitesses des deux petites particules en collision.
* Si Δt2 < Δt1 (avec éventuellement Δt1 = ∞ si aucune petite collision possible): on fait avancer toutes les particules pendant Δt2, puis on change aléatoirement l’angle des vitesses de la grosse particule et de la petite particule en collision.

Dans tous les cas, on vérifie à t + Δt  si une petite particule se trouve hors de l’environnement (carré): on la supprime et on redéfinit une petite particule aléatoirement dans l’environnement.

#### Caractéristiques du modèle
1. Prise en compte des collisions des petites particules
2. Environnement ouvert (sans rebond des petites particules), génération d’une petite particule aléatoire à chaque sortie d’une petite particule (pour avoir une densité constante)
3. Unique environnement


### Mesures 

Les outils fournissent des mesures sur les trajectoires calculées :
* Fréquence des grosses collisions
* LPM : libre parcours miyen (distance moyenne parcourue par la grosse particule entre deux collisions)
* Distance moyenne de la grosse particule par rapport à sa position initiale
* Distance maximale de la grosse particule par rapport à sa poisition initiale
* Nombres de grosses collisions

## C. Installation

Clone the respository and run `python setup.py install`, or `pip install git+https://github.com/baptiste-pasquier/brownian`.

Exécution des tests unitaires : `python -m pytest`

## D. Exemples
* Affichage d'une simulation de type 1, 2 puis 3 : [example.py](examples/example.py)

* Affichage d'une vidéo de simulation de type 2 : [movie.py](examples/movie.py)

* Calcul des statistiques en multiprocessing : [calcul1.py](examples/calcul/calcul1.py) pour le modèle 1, [calcul2.py](examples/calcul/calcul2.py) pour le modèle 2 et [calcul3.py](examples/calcul/calcul3.py) pour le modèle 3.

* Profiling des simulations : [profiler.py](examples/profiling/profiler.py)

* Affichage de plusieurs méthodes de génération aléatoire de points dans un disque : [generation_aleatoire.py](examples/generation_aleatoire.py)



## E. Utilisation

* Initialisation d'une simulation
```
from brownian.simulation1 import Simulation1
from brownian.outils import stats
a = Simulation1()
```
Il est possible de personnaliser les paramètres de la simulation, voir le fichier [example.py](examples/example.py).

* Execution d'un calcul
```
a.calcul()
```
Le paramètre `show=True` permet d'afficher les différentes étapes de la simulation.

* Affichage des statistiques du dernier calcul effectué
```
stats(a, show=True)
```

* Affichage de la trajectoire du dernier calcul effectué
```
a.traj_image()
```
Il est possible de refaire d'exécuter d'autres calculs avec les mêmes paramètres de simulation avec la commande `a.calcul()`.


## F. Fonctionnalités
List of features ready and TODOs for future development



