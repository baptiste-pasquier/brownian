# -*- coding: utf-8 -*-
from math import cos, sin, sqrt
import numpy as np

# ---------------------------------------------------------------------------- #
#                                    Outils                                    #
# ---------------------------------------------------------------------------- #


def distance(x1, y1, x2, y2):
    """
    Distance euclidienne entre les points (x1, y1) et (x2, y2)

    Arguments:
        x1 {float}
        y1 {float}
        x2 {float}
        y2 {float}

    Returns:
        float -- distance euclidienne
    """
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


# --------------------------------- Affichage -------------------------------- #

def show_listparticles_vector(ax, liste, color, x_origin=0, y_origin=0):
    """
    Outil d'affichage des vecteurs d'une liste de particules sous forme de flèche

    Arguments:
        ax {matplotlib.axes}
        liste {Particle list} -- liste des particules dont il faut afficher le vecteur vitesse
        color {string} -- couleur des vecteurs

    Keyword Arguments:
        x_origin {float} -- coordonnée x de l'origine absolue (default: {0})
        y_origin {float} -- coordonnée y de l'origine absolue (default: {0})
    """
    N = len(liste)
    X, Y, U, V = np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)
    for i in range(N):
        x, y = liste[i].x, liste[i].y
        vx, vy = liste[i].vx, liste[i].vy
        X[i] = x + x_origin
        Y[i] = y + y_origin
        U[i] = vx
        V[i] = vy

    ax.quiver(X, Y, U, V, color=color, width=0.002)


def show_listparticles_point(ax, liste, color, x_origin=0, y_origin=0, marker='.'):
    """
    Outil d'affichage d'une liste de particules sous forme de points

    Arguments:
        ax {matplotlib.axes}
        liste {Particle list} -- liste des particules à afficher
        color {string} -- couleur des vecteurs

    Keyword Arguments:
        x_origin {float} -- coordonnée x de l'origine absolue (default: {0})
        y_origin {float} -- coordonnée y de l'origine absolue (default: {0})
        marker {str} -- marqueur pour l'affichage des points (default: {'.'})
    """
    N = len(liste)
    X, Y = np.zeros(N), np.zeros(N)
    for i in range(N):
        X[i] = liste[i].x + x_origin
        Y[i] = liste[i].y + y_origin

    ax.scatter(X, Y, c=color, marker=marker)


class Particle:
    def __init__(self, x, y, speed, theta, epsilon_time):
        """
        Définition d'une particule

        Arguments:
            x {float} -- coordonnée x de la particule
            y {float} -- coordonnée y de la particule
            speed {float} -- vitesse de la particule
            theta {float} -- angle de la vitesse de la particule
            epsilon_time {float} -- précision pour les égalité de collision
        """
        self.x = x
        self.y = y
        self.vx = speed * cos(theta)
        self.vy = speed * sin(theta)
        self.epsilon_time = epsilon_time
        # On ne stocke pas speed et theta car ils sont liés à vx et vy

    def update_time(self, delta_time):
        """
        Mise à jour de la position de la particule après un intervalle de temps

        Arguments:
            delta_time {float} -- intervalle de temps
        """
        new_x = self.x + delta_time * self.vx
        new_y = self.y + delta_time * self.vy

        self.x = new_x
        self.y = new_y

    def collision(self, particle2):
        """
        Détection de collision avec une autre particule

        Arguments:
            particle2 {Particle} -- Autre particule

        Returns:
            bool -- True si collision, False sinon
            float -- Date relative de la collision, 0 sinon
        """
        vx1 = self.vx
        vy1 = self.vy
        vx2 = particle2.vx
        vy2 = particle2.vy
        x1 = self.x
        y1 = self.y
        x2 = particle2.x
        y2 = particle2.y

        try:
            tx = (x2 - x1) / (vx1 - vx2)
            ty = (y2 - y1) / (vy1 - vy2)
        except ZeroDivisionError:
            return False, 0

        # On vérifie que les dates de collisions selon x et y sont égales
        # et que la collision a lieu dans le futur
        if abs(tx - ty) < self.epsilon_time and tx > 0 and ty > 0:
            return True, tx
        else:
            return False, 0

    def change_theta(self, new_theta):
        """
        Changement de l'angle theta du vecteur vitesse de la particule

        Arguments:
            new_theta {float} -- angle theta
        """
        speed = sqrt((self.vx ** 2) + (self.vy ** 2))
        self.vx = speed * cos(new_theta)
        self.vy = speed * sin(new_theta)


# ---------------------------------------------------------------------------- #
#                                 Outils finaux                                #
# ---------------------------------------------------------------------------- #

def regular_time(X, Y, T, coeff=2, nb_image=0):
    """
    Calcul des positions à intervalle de temps régulier pour afficher une vidéo avec un temps réaliste.

    Arguments:
        X {float list} -- Coordonnées x à des temps T
        Y {float list} -- Coordonnées y à des temps T
        T {float list} -- Temps


    Keyword Arguments:
        coeff {int} -- coefficient multiplicateur pour le nombre de positions à calculer
        nb_image {int} -- nombre de positions finales (remplace coeff si nb_image != 0)

    Returns:
        {float list} -- Coordonnées x à intervalle de temps régulier
        {float list} -- Coordonnées y à intervalle de temps régulier
        {float list} -- Temps à intervalle régulier
    """
    nb = len(X) - 1

    if nb_image != 0:
        T_new = np.linspace(T[0], T[-1], nb_image)
    else:
        T_new = np.linspace(T[0], T[-1], nb * coeff + 1)

    X_new = []
    Y_new = []
    i = 0

    for i_new in range(len(T_new)):
        temps = T_new[i_new]
        while i + 1 < len(T) and temps >= T[i + 1]:
            i += 1
        if i + 1 == len(T):
            pourcentage = 0
            x = X[i]
            y = Y[i]
        else:
            pourcentage = (temps - T[i]) / (T[i + 1] - T[i])
            x = X[i] + (X[i + 1] - X[i]) * pourcentage
            y = Y[i] + (Y[i + 1] - Y[i]) * pourcentage
        X_new.append(x)
        Y_new.append(y)

    return X_new, Y_new, list(T_new)

# Exemple

# X = [0, 1, 2, 4, 10]
# Y = [0, 3, 6, 20, 30]
# T = [0, 2, 4, 5, 6]
# regular_time(X,Y,T, coeff=2)


def stats(simulation, show=False):
    """
    Calcul des mesures de simulation

    Arguments:
        simulation {Simulation1 2 ou 3} -- objet de simulation

    Keyword Arguments:
        show {bool} -- Si True : affichage des valeurs (default: {False})

    Returns:
        float -- Fréquence des grosses collisions
        float -- Distance moyenne de la grosse particule par rapport à l'origine
        float -- Distance maximake de la grosse particule par rapport à l'origine
    """

    historic = simulation.historic_BP
    X = [elem[1].x for elem in historic]
    Y = [elem[1].y for elem in historic]
    T = [elem[0] for elem in historic]

    # Frequence des collisions
    freq = (len(X) - 1) / T[-1]

    # Distance moyenne par rapport à la position initiale
    X_regul, Y_regul, _ = regular_time(X, Y, T, coeff=5)
    dist_list = [distance(0, 0, X_regul[i], Y_regul[i]) for i in range(len(X_regul))]
    dist_moy = np.sum(dist_list) / (len(X_regul) - 1)

    # Distance maximale atteinte
    dist_max = 0
    for dist in dist_list:
        if dist >= dist_max:
            dist_max = dist

    if show:
        print("Fréquence des collisions : ", freq)
        print("Distance moyenne de la grosse particule : ", dist_moy)
        print("Distance maximale de la grosse particule : ", dist_max)
    return freq, dist_moy, dist_max
