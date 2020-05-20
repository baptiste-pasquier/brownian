from .outils import Particle, show_listparticles_point, show_listparticles_vector, regular_time
from random import random
import matplotlib.pyplot as plt
import copy
from math import pi

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

