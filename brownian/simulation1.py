from .outils import Particle, show_listparticles_point, show_listparticles_vector
from random import random
import matplotlib.pyplot as plt
import copy
from math import pi, sqrt, cos, sin

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
    def __init__(self, nb_etapes=100, density=10**4, speed_BP_init=1, theta_BP_init=-pi / 4, speed=1, time_interval=0.10, epsilon_time=0.25):
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


# Méthode pour fixer les paramètres:
#     espilon time : assez faible
#     time_interval : le plus faible possible, tout en conservant un nombre faible de no_collision
#                     le but est d'avoir un disque assez grand pour avoir une grosse collision, mais
#                     assez faible pour minimiser le temps d'execution
