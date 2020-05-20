# -*- coding: utf-8 -*-
from math import cos, sin, sqrt, pi
from random import random
import matplotlib.pyplot as plt
import numpy as np
import copy


# ---------------------------------------------------------------------------- #
#                                    Outils                                    #
# ---------------------------------------------------------------------------- #


# def equal(x, y, epsilon):
#     """
#     Egalité à epsilon près entre x et y

#     Arguments:
#         x {float}
#         y {float}
#         epsilon {float} -- précision

#     Returns:
#         bool -- True si égalité, False sinon
#     """

#     if y >= x:
#         return y - x < epsilon
#     else:
#         return x - y < epsilon


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
#                             Simulation de type 1                             #
# ---------------------------------------------------------------------------- #

def random_particle(radius, speed, epsilon_time):
    """
    Génération aléatoire d'une particule dans un disque

    Arguments:
        radius {float} -- rayon du disque
        speed {float} -- vitesse de la particule
        epsilon_time {float} -- précision pour la détection de collision

    Returns:
        Particle -- particule générée
    """
    r = random()
    theta = 2 * pi * random()
    x = radius * sqrt(r) * cos(theta)
    y = radius * sqrt(r) * sin(theta)
    theta_speed = 2 * pi * random()

    return Particle(x, y, speed, theta_speed, epsilon_time)


class Workzone():
    """
    Environnement : ensemble de particules dans un disque
    """
    def __init__(self, particle_number, radius, speed, epsilon_time):
        """
        Définition d'un ensemble de particules aléatoires dans un disque

        Arguments:
            particle_number {int} -- nombre de particules
            radius {float} -- rayon du disque
            speed {float} -- vitesse des particules
            epsilon_time {float} -- précision pour la détection des collisions
        """
        self.particle_number = particle_number
        self.particles = [random_particle(radius, speed, epsilon_time) for i in range(particle_number)]

    def workzone_update_time(self, delta_time):
        """
        Mise à jour des positions de toutes les particules de la zone après un intervalle de temps

        Arguments:
            delta_time {float} -- intervalle de temps
        """
        for i in range(self.particle_number):
            self.particles[i].update_time(delta_time)


class Simulation1:
    def __init__(self, nb_etapes=100, density=10**4, speed_BP_init=1, theta_BP_init=-pi/4, speed=1, time_interval=0.10, epsilon_time=0.25):
        """
        Définition de l'espace de travail pour une simulation de type 1

        Keyword Arguments:
            nb_etapes {int} -- nombre de collisions dans la simulation (default: {100})
            density {float} -- densité surfacique de petites particules (default: {10**4})
            speed_BP_init {float} -- vitesse de la grosse particule (default: {1})
            theta_BP_init {float} -- angle de la vitesse intiale de la grosse particule (default: {-pi/4})
            speed {float} -- vitesse des petites particules (default: {1})
            time_interval {float} -- intervalle de temps maximal pour une grosse collision (default: {0.10})
            epsilon_time {float} -- précision pour la détection des collisions (default: {0.25})
        """

        # Rayon et nombre de particules de chaque disque
        self.radius = (speed_BP_init + speed) * time_interval
        self.particle_number = int(density * pi * (self.radius ** 2))

        self.speed_BP_init = speed_BP_init
        self.theta_BP_init = theta_BP_init
        self.speed = speed
        self.time_interval = time_interval
        self.nb_etapes = nb_etapes
        self.epsilon_time = epsilon_time

        self.title = "Simulation de type 1"

    def calcul(self, show=False, vector=True, pause=1, coeff_affichage=1):
        """
        Calcul d'une simulation

        Keyword Arguments:
            show {bool} -- si True : affichage de chaque étape (default: {False})
            vector {bool} -- si True : affichage des vecteurs vitesses (si show=True) (default: {True})
            pause {float} -- délai entre chaque affichage (si show=True) (default: {1})
            coeff_affichage {float} -- zoom de l'affichage (si show=True) (default: {1})

        Sauvegarde dans la classe Simulation1:
            self.historic_BP {(float, Particle) list} -- historique des temps et de la grosse particule à chaque collision
            self.nb_no_collision {int} -- Nombre d'absences de collision au cours de la simulation
        """
        if show:
            fig, ax = plt.subplots()

        time = 0
        nb_collision = 0
        nb_no_collision = 0     # Nombre d'absences de collision

        # Initialisation de la grosse particule
        BP = Particle(0, 0, self.speed_BP_init, self.theta_BP_init, self.epsilon_time)

        # Initialisation de l'historique de la grosse particule
        historic_BP = []
        historic_BP.append((time, copy.copy(BP)))

        # Boucle de calcul des grosses collisions
        while nb_collision < self.nb_etapes:
            # Définition d'un nouvel environnement
            zone = Workzone(self.particle_number, self.radius, self.speed, self.epsilon_time)
            # Définition de la grosse particule en coordonnées relatives dans cet environnement
            BP_in_zone = copy.copy(BP)
            BP_in_zone.x = 0    # Grosse particule à l'origine dans chaque environnement
            BP_in_zone.y = 0

            # Sauvegarde de la position de la grosse particule
            x_origin, y_origin = BP.x, BP.y

            if show:
                #####
                ax.clear()

                X = [elem[1].x for elem in historic_BP]
                Y = [elem[1].y for elem in historic_BP]
                plt.plot(X, Y, color='red')

                circ = plt.Circle((BP.x, BP.y), radius=self.radius, color='orange', fill=False)
                ax.add_artist(circ)
                show_listparticles_vector(ax, zone.particles, 'blue', BP.x, BP.y)
                show_listparticles_vector(ax, [BP], 'red')

                plt.grid()
                plt.xlim(-coeff_affichage * self.radius, coeff_affichage * self.radius)
                plt.ylim(-coeff_affichage * self.radius, coeff_affichage * self.radius)
                plt.title(self.title + '\nt=' + str(round(time, 4)))
                plt.draw()
                plt.pause(pause)
                #####

            # Calcul de la première collision
            t_min = self.time_interval
            i_argmin = -1
            for i in range(self.particle_number):
                collision, t = BP_in_zone.collision(zone.particles[i])
                if collision and t <= t_min:
                    t_min = t
                    i_argmin = i

            # Si pas de grosse collision
            if i_argmin == -1:
                delta_time = self.time_interval
                BP.update_time(delta_time)
                nb_no_collision += 1

            # Si grosse collision possible
            else:
                nb_collision += 1
                delta_time = t_min  # Date relative de la collision
                BP.update_time(delta_time)

                # Changement de l'angle de la vitesse de la grosse particule
                new_theta = 2 * pi * random()
                BP.change_theta(new_theta)

                # Sauvegarde de la grosse particule dans l'historique
                historic_BP.append((time + delta_time, copy.copy(BP)))   # Seulement collision dans historique

            # Mise à jour du temps et de l'environnement
            time += delta_time
            zone.workzone_update_time(delta_time)

            if show:
                ####
                ax.clear()

                X = [elem[1].x for elem in historic_BP]
                Y = [elem[1].y for elem in historic_BP]
                plt.plot(X, Y, color='red')

                show_listparticles_point(ax, zone.particles, 'blue', x_origin, y_origin)
                if i_argmin == -1:
                    show_listparticles_point(ax, [BP], 'red', marker='o')
                else:
                    show_listparticles_point(ax, [BP], 'fuchsia', marker='*')
                    circ = plt.Circle((BP.x, BP.y), radius=self.radius * coeff_affichage / 15, color='fuchsia', fill=False)
                    ax.add_artist(circ)

                plt.grid()
                plt.xlim(-coeff_affichage * self.radius, coeff_affichage * self.radius)
                plt.ylim(-coeff_affichage * self.radius, coeff_affichage * self.radius)
                plt.title(self.title + '\nt=' + str(round(time, 4)))
                plt.draw()
                plt.pause(pause)
                #####

        # print("No collision : ", nb_no_collision)
        if show:
            plt.close()

        # Sauvegarde de l'historique de la grosse particule et du nombre d'absence de collision.
        self.historic_BP = historic_BP
        self.nb_no_collision = nb_no_collision

    def traj_image(self, coeff_affichage=1):
        """
        Affichage de la trajectoire d'une simulation
        Nécessite d'avoir exécuté un calcul avant

        Keyword Arguments:
            coeff_affichage {float} -- zoom de l'affichage (default: {1})
        """
        historic = self.historic_BP
        fig, ax = plt.subplots()
        X = [elem[1].x for elem in historic]
        Y = [elem[1].y for elem in historic]

        plt.plot(X, Y)
        plt.grid()
        plt.xlim(-coeff_affichage * self.radius, coeff_affichage * self.radius)
        plt.ylim(-coeff_affichage * self.radius, coeff_affichage * self.radius)
        plt.title(self.title)
        plt.show()


# Méthode pour fixer les valeurs:
#     espilon time : assez faible
#     time_interval : le plus faible possible, tout en conservant un nombre faible de no_collision


# ---------------------------------------------------------------------------- #
#                             Simulation de type 2                             #
# ---------------------------------------------------------------------------- #

def random_particle_square(dim, speed, epsilon_time):
    """
    Génération aléatoire d'une particule dans un carré

    Arguments:
        dim {float} -- carrée de côté 2*dim
        speed {float} -- vitesse de la particule
        epsilon_time {float} -- précision pour la détection de collision

    Returns:
        Particle -- particule générée
    """
    x = -dim + 2 * dim * random()
    y = -dim + 2 * dim * random()
    theta_speed = 2 * pi * random()

    return Particle(x, y, speed, theta_speed, epsilon_time)


class Workzone_square():
    """
    Environnement : ensemble de particules dans un carré
    """
    def __init__(self, particle_number, dim, speed, epsilon_time):
        """
        Définition d'un ensemble de particules aléatoires dans un carré

        Arguments:
            particle_number {int} -- nombre de particules
            dim {float} -- carré de côté 2*dim
            speed {float} -- vitesse des particules
            epsilon_time {float} -- précision pour la détection de collision
        """
        self.particle_number = particle_number
        self.dim = dim
        self.speed = speed
        self.epsilon_time = epsilon_time

        self.particles = [random_particle_square(dim, speed, epsilon_time) for i in range(particle_number)]

    def workzone_update_time(self, delta_time):
        """
        Mise à jour des positions de toutes les particules après un intervalle de temps

        Arguments:
            delta_time {float} -- intervalle de temps
        """
        for i in range(self.particle_number):
            self.particles[i].update_time(delta_time)

    def delete_outside(self):
        """
        Suppression des particules en dehors de la zone
        Génération d'une nouvelle particule aléatoire pour chaque sortie

        Returns:
            int list -- indices des particules supprimées (pour affichage particulier)
        """
        indices_suppression = []
        for i in range(self.particle_number):
            if abs(self.particles[i].x) > self.dim or abs(self.particles[i].y) > self.dim:
                self.particles[i] = random_particle_square(self.dim, self.speed, self.epsilon_time)
                indices_suppression.append(i)
        return indices_suppression


class NoBigCollision(Exception):
    """
    Aucune grosse collision trouvée
    """
    pass


class OutsideEnv(Exception):
    """
    Grosse particule en dehors de la zone
    """
    pass


class Simulation2:
    def __init__(self, nb_etapes=200, density=10**4, speed_BP_init=1, theta_BP_init=-pi / 4, speed=1, dim=0.2, epsilon_time=0.005):
        """
        Définition de l'espace de travail pour une simulation de type 2

        Keyword Arguments:
            nb_etapes {int} -- nombre de collisions dans la simulation (default: {200})
            density {float} -- densité surfacique de petites particules (default: {10**4})
            speed_BP_init {float} -- vitesse de la grosse particule (default: {1})
            theta_BP_init {float} -- angle de la vitesse intiale de la grosse particule (default: {-pi/4})
            speed {float} -- vitesse des petites particules (default: {1})
            dim {float} -- environnement carré de côté 2*dim (default: {0.2})
            epsilon_time {float} -- précision pour la détection des collisions (default: {0.005})
        """

        # Nombre de particules dans l'environnement
        self.particle_number = int(density * 4 * dim**2)

        self.speed_BP_init = speed_BP_init
        self.theta_BP_init = theta_BP_init
        self.speed = speed
        self.nb_etapes = nb_etapes
        self.dim = dim
        self.epsilon_time = epsilon_time

        self.title = "Simulation de type 2"

    def calcul(self, show=False, vector=True, pause=0.25, coeff_affichage=1, movie=False):
        """
        Calcul d'une simulation

        Keyword Arguments:
            show {bool} -- si True : affichage de chaque étape (default: {False})
            vector {bool} -- si True : affichage des vecteurs vitesses (si show=True) (default: {True})
            pause {float} -- délai entre chaque affichage (si show=True) (default: {0.25})
            coeff_affichage {float} -- zoom de l'affichage (si show=True) (default: {1})
            movie {bool} -- si True : sauvegarde de l'environnement pour créer une vidéo (default: {False})

        Raises:
            NoBigCollision: Aucune grosse collision n'est possible dans le futur
            OutsideEnv: Grosse particule en dehors de la zone

        Sauvegarde dans la classe Simulation2:
            self.historic_BP {(float, Particle) list} -- historique du temps et de la grosse particule à chaque collision
            self.historic_PP {(float, Workzone_square) list} -- (Si movie=True) historique temps et de l'environnement à chaque collision
        """
        if show:
            fig, ax = plt.subplots()
            plt.grid()
            plt.xlim(-self.dim, self.dim)
            plt.ylim(-self.dim, self.dim)

        time = 0
        nb_collision = 0

        # Initialisation de la grosse particule
        BP = Particle(0, 0, self.speed_BP_init, self.theta_BP_init, self.epsilon_time)

        # Initialisation de l'historique de la grosse particule
        historic_BP = []
        historic_BP.append((time, copy.copy(BP)))

        # Initialisation de l'environnement unique
        zone = Workzone_square(self.particle_number, self.dim, self.speed, self.epsilon_time)

        # Initialisation de l'historique des petites particules pour la vidéo
        if movie:
            historic_PP = []
            historic_PP.append((time, copy.deepcopy(zone)))

        # Boucle de calcul des grosses collisions
        while nb_collision < self.nb_etapes:
            if show and vector:
                ####
                ax.clear()

                X = [elem[1].x for elem in historic_BP]
                Y = [elem[1].y for elem in historic_BP]
                plt.plot(X, Y, color='red')

                show_listparticles_vector(ax, zone.particles, 'blue')
                show_listparticles_vector(ax, [BP], 'red')

                plt.title(self.title + '\nt=' + str(round(time, 4)))
                plt.xlim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
                plt.ylim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
                plt.draw()
                plt.pause(pause)
                #####

            # Calcul de la première collision
            t_min = float("inf")
            i_argmin = -1
            for i in range(self.particle_number):
                collision, t = BP.collision(zone.particles[i])
                if collision and t <= t_min:
                    t_min = t
                    i_argmin = i

            # Si pas de grosse collision
            if i_argmin == -1:
                raise NoBigCollision

            # Si grosse collision possible
            else:
                nb_collision += 1
                delta_time = t_min      # Date relative de la collision

                # Mise à jour du temps et de l'environnement
                time += delta_time
                zone.workzone_update_time(delta_time)
                BP.update_time(delta_time)

                # Changement de l'angle de la vitesse de la grosse particule
                new_theta = 2 * pi * random()
                BP.change_theta(new_theta)

                # Changement de l'angle de la vitesse de la petite particule percutée
                PP = zone.particles[i_argmin]
                new_theta = 2 * pi * random()
                PP.change_theta(new_theta)

                # Sauvegarde de la grosse particule dans l'historique
                historic_BP.append((time, copy.copy(BP)))   # Seulement collision dans historique

                if movie:
                    historic_PP.append((time, copy.deepcopy(zone)))

                # Supression des particules en dehors de l'environnement et régénération
                indices_suppression = zone.delete_outside()

                if movie:
                    historic_PP.append((time, copy.deepcopy(zone)))

                # Vérification que la grosse particule est toujours dans l'environnement
                if abs(BP.x) > self.dim or abs(BP.y) > self.dim:
                    raise OutsideEnv

            if show:
                ####
                ax.clear()

                X = [elem[1].x for elem in historic_BP]
                Y = [elem[1].y for elem in historic_BP]
                plt.plot(X, Y, color='red')

                show_listparticles_point(ax, zone.particles, 'blue')
                show_listparticles_point(ax, [zone.particles[i] for i in indices_suppression], 'green')
                if i_argmin == -1:
                    show_listparticles_point(ax, [BP], 'red', marker='o')
                else:
                    show_listparticles_point(ax, [BP], 'fuchsia', marker='*')
                    circ = plt.Circle((BP.x, BP.y), radius=self.dim * coeff_affichage / 15, color='fuchsia', fill=False)
                    ax.add_artist(circ)

                plt.title(self.title + '\nt=' + str(round(time, 4)))
                plt.xlim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
                plt.ylim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
                plt.draw()
                plt.pause(pause)
                #####

        if show:
            plt.close()

        # Sauvegarde de l'historique de la grosse particule
        self.historic_BP = historic_BP
        # Sauvegarde de l'historique des petites particules pour la vidéo
        if movie:
            self.historic_PP = historic_PP

    def traj_image(self, coeff_affichage=1):
        """
        Affichage de la trajectoire d'une simulation
        Nécessite d'avoir exécuté un calcul avant.

        Keyword Arguments:
            coeff_affichage {float} -- zoom de l'affichage (default: {1})
        """
        historic = self.historic_BP
        fig, ax = plt.subplots()
        X = [elem[1].x for elem in historic]
        Y = [elem[1].y for elem in historic]

        plt.plot(X, Y)
        plt.grid()
        plt.xlim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
        plt.ylim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
        plt.title(self.title)
        plt.show()

    def movie(self, coeff_affichage=1, nb_images=300):
        """
        Affichage d'une vidéo de simulation
        Nécessite d'avoir exécuté un calcul avant, avec l'option movie activée.

        Keyword Arguments:
            coeff_affichage {float} -- zoom de l'affichage (default: {1})
            nb_images {int} -- nombres d'images pour la vidéo (default: {300})
        """
        historic_BP = self.historic_BP
        historic_PP = self.historic_PP
        fig, ax = plt.subplots()

        X = [elem[1].x for elem in historic_BP]
        Y = [elem[1].y for elem in historic_BP]
        T = [elem[0] for elem in historic_BP]

        X_new, Y_new, T_new = regular_time(X, Y, T, nb_image=nb_images)

        ppx = [[] for image in range(nb_images)]
        ppy = [[] for image in range(nb_images)]

        Tpp = [historic_PP[temps][0] for temps in range(len(historic_PP))]

        for id_particle in range(self.particle_number):
            Xpp = [historic_PP[temps][1].particles[id_particle].x for temps in range(len(historic_PP))]
            Ypp = [historic_PP[temps][1].particles[id_particle].y for temps in range(len(historic_PP))]
            Xpp_new, Ypp_new, _ = regular_time(Xpp, Ypp, Tpp, nb_image=nb_images)

            for image in range(nb_images):
                ppx[image].append(Xpp_new[image])
                ppy[image].append(Ypp_new[image])

        for i in range(len(X_new)):
            ax.clear()
            ax.scatter(ppx[i], ppy[i])
            ax.plot(X_new[:i], Y_new[:i], color='magenta')
            ax.scatter(X_new[i], Y_new[i], color='red', marker='o')
            plt.grid()
            plt.xlim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
            plt.ylim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
            plt.title(self.title + '\nt=' + str(round(T_new[i], 4)))
            plt.draw()
            plt.pause(0.00001)


# Méthode pour fixer les valeurs:
#     espilon time : assez faible
#     dim : le plus faible possible, tout en conservant l'indicateur OutsideEnv nul


# ---------------------------------------------------------------------------- #
#                             Simulation de type 3                             #
# ---------------------------------------------------------------------------- #

class Workzone_square_v2(Workzone_square):
    """
    Ajout d'une fonctionnalité de détection de collision entre toutes
    les particules de la zone.
    """
    def __init__(self, particle_number, dim, speed, epsilon_time):
        super().__init__(particle_number, dim, speed, epsilon_time)

    def collision_zone(self):
        """
        Détection de la première collision dans toute la zone

        Returns:
            bool -- True si collision, False sinon
            float -- Date relative de la collision, 0 sinon
            int, int tuple -- Indices des particules en collision, (-1, -1) sinon
        """
        t_min = float("inf")
        indices = -1, -1
        for i in range(0, self.particle_number - 1):
            for j in range(i + 1, self.particle_number):
                collision, t = self.particles[i].collision(self.particles[j])
                if collision and t < t_min:
                    t_min = t
                    indices = i, j

        # Si aucune collision dans la zone
        if indices == (-1, -1):
            return False, 0, indices

        # Si petite collision dans la zone
        else:
            return True, t_min, indices


class NoBigLittleCollision(Exception):
    """
    Aucune grosse collision ou petite collision trouvée
    """
    pass


class Simulation3:
    def __init__(self, nb_etapes=200, density=10**4, speed_BP_init=1, theta_BP_init=-pi / 4, speed=1, dim=0.2, epsilon_time=0.005, limit_collision_zone=1):
        """
        Définition de l'espace de travail pour une simulation de type 3

        Keyword Arguments:
            nb_etapes {int} -- nombre de collisions dans la simulation (default: {200})
            density {float} -- densité surfacique de petites particules (default: {10**4})
            speed_BP_init {float} -- vitesse de la grosse particule (default: {1})
            theta_BP_init {float} -- angle de la vitesse intiale de la grosse particule (default: {-pi/4})
            speed {float} -- vitesse des petites particules (default: {1})
            dim {float} -- environnement carré de côté 2*dim (default: {0.2})
            epsilon_time {float} -- précision pour la détection des collisions (default: {0.005})
            limit_collision_zone {float} -- coefficient pour réduire le nombre de petites collisions (default: {1})
        """

        # Nombre de particules dans l'environnement
        self.particle_number = int(density * 4 * dim**2)

        self.speed_BP_init = speed_BP_init
        self.theta_BP_init = theta_BP_init
        self.speed = speed
        self.nb_etapes = nb_etapes
        self.dim = dim
        self.epsilon_time = epsilon_time
        self.limit_collision_zone = limit_collision_zone

        self.title = "Simulation de type 3"

    def calcul(self, show=False, vector=True, pause=0.5, coeff_affichage=1):
        """
        Calcul d'une simulation
        Peut boucler à l'infini si beaucoup de petites collisions et peu de collision

        Keyword Arguments:
            show {bool} -- si True : affichage de chaque étape (default: {False})
            vector {bool} -- si True : affichage des vecteurs vitesses (si show=True) (default: {True})
            pause {float} -- délai entre chaque affichage (si show=True) (default: {0.5})
            coeff_affichage {float} -- zoom de l'affichage (si show=True) (default: {1})

        Raises:
            NoBigLittleCollision: Aucune grosse ou petite collision n'est possible dans le futur
            OutsideEnv: Grosse particule en dehors de la zone

        Sauvegarde dans la classe Simulation3:
            self.historic_BP {(float, Particle) list} -- historique du temps et de la grosse particule à chaque collision
        """
        if show:
            fig, ax = plt.subplots()
            plt.grid()
            plt.xlim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
            plt.ylim(-coeff_affichage * self.dim, coeff_affichage * self.dim)

        time = 0
        nb_collision = 0

        # Initialisation de la grosse particule
        BP = Particle(0, 0, self.speed_BP_init, self.theta_BP_init, self.epsilon_time)

        # Initialisation de l'historique de la grosse particule
        historic_BP = []
        historic_BP.append((time, copy.copy(BP)))

        # Historique distant pour le show car sauvegarde même lorsque pas de grosse collision
        if show:
            historic_BP_show = []
            historic_BP_show.append((time, copy.copy(BP)))

        # Initialisation de l'unique environnement
        zone = Workzone_square_v2(self.particle_number, self.dim, self.speed, self.epsilon_time / self.limit_collision_zone)

        # Boucle de calcul des grosses collisions
        while nb_collision < self.nb_etapes:
            if show and vector:
                ####
                ax.clear()

                X = [elem[1].x for elem in historic_BP_show]
                Y = [elem[1].y for elem in historic_BP_show]
                plt.plot(X, Y, color='red')

                show_listparticles_vector(ax, zone.particles, 'blue')
                show_listparticles_vector(ax, [BP], 'red')

                plt.title(self.title + '\nt=' + str(round(time, 4)))
                plt.xlim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
                plt.ylim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
                plt.draw()
                plt.pause(pause)
                #####

            # Boucle des petites collision
            while True:
                # Calcul de la premiere petite collision dans la zone
                collision_zone, t_zone, indices = zone.collision_zone()

                # Calcul de la première grosse collision
                t_min = float("inf")
                i_argmin = -1
                for i in range(self.particle_number):
                    collision, t = BP.collision(zone.particles[i])
                    if collision and t <= t_min:
                        t_min = t
                        i_argmin = i

                # Cas 1 : aucune petite collision, aucune grosse collision
                if t_zone == float("inf") and t_min == float("inf"):
                    raise NoBigLittleCollision

                # Cas 2 : petite collision (zone) avant grosse collision
                # ou : petite collision et pas de grosse collision (t_zone != inf et t_min = inf)
                elif t_zone < t_min:
                    delta_time = t_zone

                    # Mise à jour du temps, de la zone et de la grosse particule
                    time += delta_time
                    zone.workzone_update_time(delta_time)
                    BP.update_time(delta_time)

                    # Changement de l'angle de la vitesse des 2 petites particule percutées
                    PP1 = zone.particles[indices[0]]
                    PP2 = zone.particles[indices[1]]

                    new_theta1 = 2 * pi * random()
                    new_theta2 = 2 * pi * random()
                    PP1.change_theta(new_theta1)
                    PP2.change_theta(new_theta2)

                    # Sauvegarde de la grosse particule dans l'historique (seulement show)
                    if show:
                        historic_BP_show.append((time, copy.copy(BP)))
                    # Pas de sauvegarde dans l'autre historique car seulement grosse collision

                    # Supression des particules en dehors de l'environnement et régénération
                    indices_suppression = zone.delete_outside()

                    # Vérification grosse particule toujours dans l'environnement
                    if abs(BP.x) > self.dim or abs(BP.y) > self.dim:
                        raise OutsideEnv

                    if show:
                        ####
                        ax.clear()

                        X = [elem[1].x for elem in historic_BP_show]
                        Y = [elem[1].y for elem in historic_BP_show]
                        plt.plot(X, Y, color='red')

                        show_listparticles_point(ax, zone.particles, 'blue')
                        show_listparticles_point(ax, [zone.particles[i] for i in indices_suppression], 'green')
                        show_listparticles_point(ax, [zone.particles[i] for i in indices], 'fuchsia', marker='*')
                        circ = plt.Circle((zone.particles[indices[0]].x, zone.particles[indices[0]].y), radius=self.dim * coeff_affichage / 15, color='fuchsia', fill=False)
                        ax.add_artist(circ)
                        show_listparticles_point(ax, [BP], 'red', marker='o')

                        plt.title(self.title + '\nt=' + str(round(time, 4)))
                        plt.xlim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
                        plt.ylim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
                        plt.draw()
                        plt.pause(pause)
                        #####

                # Cas 3 : grosse collision avant petite collision
                # ou grosse collision et pas de petite collision (t_zone = inf)
                elif t_min <= t_zone and t_min < float('inf'):
                    nb_collision += 1
                    delta_time = t_min

                    # Mise à jour du temps, de la zone et de la grosse particule
                    time += delta_time
                    zone.workzone_update_time(delta_time)
                    BP.update_time(delta_time)

                    # Changement de l'angle de la vitesse de la grosse particule
                    new_theta = 2 * pi * random()
                    BP.change_theta(new_theta)

                    # Changement de l'angle de la vitesse de la petite particule percutée
                    PP = zone.particles[i_argmin]
                    new_theta = 2 * pi * random()
                    PP.change_theta(new_theta)

                    # Sauvegarde de la grosse particule dans l'historique
                    historic_BP.append((time, copy.copy(BP)))
                    if show:
                        historic_BP_show.append((time, copy.copy(BP)))

                    # Supression des particules en dehors de l'environnement et régénération
                    indices_suppression = zone.delete_outside()

                    # Vérification grosse particule toujours dans l'environnement
                    if abs(BP.x) > self.dim or abs(BP.y) > self.dim:
                        raise OutsideEnv

                    if show:
                        ####
                        ax.clear()

                        X = [elem[1].x for elem in historic_BP_show]
                        Y = [elem[1].y for elem in historic_BP_show]
                        plt.plot(X, Y, color='red')

                        show_listparticles_point(ax, zone.particles, 'blue')
                        show_listparticles_point(ax, [zone.particles[i] for i in indices_suppression], 'green')
                        show_listparticles_point(ax, [BP], 'fuchsia', marker='*')
                        circ = plt.Circle((BP.x, BP.y), radius=self.dim * coeff_affichage / 15, color='fuchsia', fill=False)
                        ax.add_artist(circ)
                        plt.title(self.title + '\nt=' + str(round(time, 4)))
                        plt.xlim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
                        plt.ylim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
                        plt.draw()
                        plt.pause(pause)
                        #####

                break   # On sort de la boucle While true car on a obtenu une grosse collision

        if show:
            plt.close()

        # Sauvegarde de l'historique de la grosse particule
        self.historic_BP = historic_BP

    def traj_image(self, coeff_affichage=1):
        """
        Affichage de la trajectoire d'une simulation
        Nécessite d'avoir exécuté un calcul avant.

        Keyword Arguments:
            coeff_affichage {float} -- zoom de l'affichage (default: {1})
        """
        historic = self.historic_BP
        fig, ax = plt.subplots()
        X = [elem[1].x for elem in historic]
        Y = [elem[1].y for elem in historic]

        plt.plot(X, Y)
        plt.grid()
        plt.xlim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
        plt.ylim(-coeff_affichage * self.dim, coeff_affichage * self.dim)
        plt.title(self.title)
        plt.show()


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
