# -*- coding: utf-8 -*-
import math
import random

from matplotlib import pyplot as plt

# --------------------------------------------------------------------------- #
#                             Simulation de type 1_1                          #
# ----------------------------------------------------------------------------#


class BrownianMotion1_1():
    """
    Objet simulation de type 1_1.

    Paramètres fondamentaux :
        n_etoile {float} : densité surfacique de particules (par défaut :
        {10**4})
        V {float} : vitesse (en norme) de la grosse particule (par défaut :
        {1})
        v {float} : vitesse (en norme) des petites particules (par défaut :
        {10})
        h {float} : durée d'une étape (par défaut : {10**-2})
        theta {float} : angle initial du vecteur vitesse de la grosse particule
        epsilon {float} : précision pour la détection des collision, est relié
        directement aux rayons des petites et de la grosse particules
    """
    def __init__(self, n_etoile=10**4, V=1, v=10, h=10**-2,
                 theta=random.uniform(-math.pi, math.pi), epsilon=10**-2):
        self.n_etoile = n_etoile
        self.V = V
        self.v = v
        self.h = h

        # rayon du disque local au début de l'étape
        self.R = self.h * (self.v + self.V)
        # (i.e. particules susceptibles de rencontrer la grosse)

        # conditions initiales grosse particule
        self.Particule_X = [0]
        self.Particule_Y = [0]
        self.Vitesse_X = [self.V * math.cos(theta)]
        self.Vitesse_Y = [self.V * math.sin(theta)]

        # positions de la grosse particule à chaque collision (et au point de
        # départ)
        self.CollisionsX = [0]
        self.CollisionsY = [0]

        # précision souhaitée
        self.epsilon = epsilon

    def generEnvironment(self, e, R):
        """
        Génère aléatoirement les particules dans le disque local de la grosse
        durant l'étape e.

        Arguments :
            e {int} : indice désignant l'étape durant laquelle on travaille
            R {float} : rayon du disque local

        Le vrai temps correspondant à e est t=e*h + Delta_t, où Delta_t est le
        temps écoulé depuis le début de l'étape.
        """
        self.particules_X = []
        self.particules_Y = []
        self.vitesses_X = []
        self.vitesses_Y = []

        S = math.pi * R**2
        N = int(S * self.n_etoile)

        for _ in range(N):
            u = random.uniform(0, 1)
            # vient du changement de variable polaire, pour
            r = R * math.sqrt(u)
            # avoir une loi unif dans le cercle
            theta = random.uniform(-math.pi, math.pi)
            self.particules_X.append(r * math.cos(theta) + self.Particule_X[e])
            self.particules_Y.append(r * math.sin(theta) + self.Particule_Y[e])

            theta = random.uniform(-math.pi, math.pi)
            self.vitesses_X.append(self.v * math.cos(theta))
            self.vitesses_Y.append(self.v * math.sin(theta))

    def show(self, e, fig, ax):
        """
        Affiche la situation a l’étape e.
        La trajectoire n'est actualisée qu'à chaque collision,
        mais les positions et vitesses sont données à chaque étape.

        Arguments :
            e {int} : indice désignant l'étape durant laquelle on travaille
            fig {matplotlib.figure.Figure} : figure de tracé
            ax {matplotlib.axes._subplots.AxesSubplot} : axe de tracé
        """
        ax.clear()
        circle = plt.Circle((self.Particule_X[e], self.Particule_Y[e]), self.R)
        circle.fill = False
        _ = ax.quiver(self.particules_X, self.particules_Y,
                      self.vitesses_X, self.vitesses_Y,
                      units='xy', color='blue')
        _ = ax.quiver(self.Particule_X[e], self.Particule_Y[e],
                      self.Vitesse_X[e], self.Vitesse_Y[e],
                      units='xy', color='red')
        _ = ax.plot(self.CollisionsX, self.CollisionsY, color='purple')
        ax.add_artist(circle)
        plt.draw()
        plt.pause(0.1)

    def collision(self, i, e):
        """
        Renvoie True et l'instant de collision si la grosse particule rencontre
        la petite particule i entre les étapes e et e+1.
        Renvoie False et 0 sinon.

        Arguments :
            i {int} : indice désignant une petite particule de l'environnement
            e {int} : indice désignant l'étape durant laquelle on travaille
        """
        vx = self.vitesses_X[i]
        vy = self.vitesses_Y[i]
        Vx = self.Vitesse_X[e]
        Vy = self.Vitesse_Y[e]
        x = self.particules_X[i]
        y = self.particules_Y[i]
        X = self.Particule_X[e]
        Y = self.Particule_Y[e]

        try:
            t1 = (x - X) / (Vx - vx)
            t2 = (y - Y) / (Vy - vy)
        except ZeroDivisionError:  # si Vx = vx ou Vy = vy,
            # les particules ne peuvent se rencontrer
            return False, 0

        # on regarde si les particules se rencontrent entre t et t+h
        if abs(t1 - t2) <= self.epsilon and 0 < t1 <= self.h:
            return True, t1
        else:
            return False, 0

    def nextPos(self, e):
        """
        Calcule la position et la vitesse de la grosse particule à l'étape e+1
        en prenant en compte toutes les collisions : celles-ci sont
        sauvegardées dans les attributs CollisionsX et CollisionsY.

        Argument :
            e {int} : indice désignant l'étape durant laquelle on travaille
        """
        # calcul de la première collision et du temps correspondant
        t_min = self.h
        i_argmin = -1
        for i in range(len(self.particules_X)):
            collision, t = self.collision(i, e)
            if collision and t <= t_min:
                t_min = t
                i_argmin = i

        duree = t_min  # pour que la durée de l'étape ne dépasse pas h

        # s'il n'y a aucune collision
        if i_argmin == -1:
            vX = self.Vitesse_X[e]
            vY = self.Vitesse_Y[e]
            posX = self.Particule_X[e] + self.h * vX
            posY = self.Particule_Y[e] + self.h * vY
            return posX, posY, vX, vY

        else:  # s'il y en a une on commence par l'amener au point d'impact
            self.Particule_X[e] += t_min * self.Vitesse_X[e]
            self.Particule_Y[e] += t_min * self.Vitesse_Y[e]
            self.CollisionsX.append(self.Particule_X[e])
            self.CollisionsY.append(self.Particule_Y[e])
            # et on change sa direction ainsi que l'environnement
            self.generEnvironment(e, self.R - self.V * duree)
            theta = random.uniform(-math.pi, math.pi)
            self.Vitesse_X[e] = self.V * math.cos(theta)
            self.Vitesse_Y[e] = self.V * math.sin(theta)

        while i_argmin != -1:  # et on regarde s'il y a d'autres collisions
            i_argmin = -1
            for i in range(len(self.particules_X)):
                collision, t = self.collision(i, e)
                if collision and t <= self.h - duree:
                    t_min = t
                    i_argmin = i
            if i_argmin == -1:  # s'il n'y en a plus
                vX = self.Vitesse_X[e]
                vY = self.Vitesse_Y[e]
                posX = self.Particule_X[e] + (self.h - duree) * vX
                posY = self.Particule_Y[e] + (self.h - duree) * vY
                return posX, posY, vX, vY
            else:  # s'il en reste
                # on fait avancer la particule jusqu'à son point d'impact
                self.Particule_X[e] += t_min * self.Vitesse_X[e]
                self.Particule_Y[e] += t_min * self.Vitesse_Y[e]
                self.CollisionsX.append(self.Particule_X[e])
                self.CollisionsY.append(self.Particule_Y[e])
                duree += t_min  # la durée augmente
                # et on change la direction et l'environnement
                self.generEnvironment(e, self.R - self.V * duree)
                theta = random.uniform(-math.pi, math.pi)
                self.Vitesse_X[e] = self.V * math.cos(theta)
                self.Vitesse_Y[e] = self.V * math.sin(theta)

    def simulationAnimated(self, nb_etapes):
        """
        Exécute une simulation animée de nb_etapes étapes.

        Argument:
            nb_etapes {int} : nombre total d'étapes que doit comporter la
            simulation

        nb_etapes est directement relié à la durée théorique de la simulation
        par la formule : durée_totale = nb_etapes * h
        """
        fig, ax = plt.subplots()
        for e in range(nb_etapes):
            self.generEnvironment(e, self.R)
            self.show(e, fig, ax)
            posX, posY, vX, vY = self.nextPos(e)
            self.Particule_X.append(posX)
            self.Particule_Y.append(posY)
            self.Vitesse_X.append(vX)
            self.Vitesse_Y.append(vY)
        plt.show()

    def simulation(self, nb_etapes):
        """
        Effectue une simulation non animée de nb_etapes étapes.

        Argument:
            nb_etapes {int} : nombre total d'étapes que doit comporter la
            simulation

        Renvoie les listes X et Y correspondant respectivement aux abscisses
        et ordonnées des collisions de la grosse particule avec des petites
        (on considère le point de départ comme étant une collision).
        """
        self.__init__(n_etoile=self.n_etoile, V=self.V, v=self.v,
                      h=self.h, epsilon=self.epsilon)  # on réinitialise
        for e in range(nb_etapes):
            self.generEnvironment(e, self.R)
            posX, posY, vX, vY = self.nextPos(e)
            self.Particule_X.append(posX)
            self.Particule_Y.append(posY)
            self.Vitesse_X.append(vX)
            self.Vitesse_Y.append(vY)
        return self.CollisionsX, self.CollisionsY


if __name__ == '__main__':
    MVT = BrownianMotion1_1(
        epsilon=10**-4, n_etoile=10**4, v=10, V=1, h=10**-2)
    MVT.simulationAnimated(100)
