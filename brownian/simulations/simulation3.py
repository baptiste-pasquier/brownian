from .outils import Particle, show_listparticles_point, show_listparticles_vector
from .simulation2 import Workzone_square, OutsideEnv
from random import random
import matplotlib.pyplot as plt
import copy
from math import pi

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
