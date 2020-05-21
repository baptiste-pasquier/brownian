import math
import pandas as pd
from matplotlib import pyplot as plt


def lpm(X, Y):
    """
    Renvoie le libre parcours moyen d'une simulation.

    X et Y sont les listes contenant respectivement les abscisses et ordonnées
    des collisions d'une simulation.
    """
    S = 0  # somme des longueurs des segments
    for i in range(len(X)-1):
        longueur = math.sqrt((X[i+1] - X[i])**2 + (Y[i+1] - Y[i])**2)
        S += longueur
    return S / (len(X) - 1)


def lpms(LX, LY):
    """
    Renvoie la liste des lpm de chacune des simulations.

    LX est une liste contenant les listes des abscisses des collisions de
    chaque simulation.
    LY est une liste contenant les listes des ordonnées des collisions de
    chaque simulation.
    """
    LPM = []
    for i in range(len(LX)):
        LPM.append(lpm(LX[i], LY[i]))
    return LPM


def distance(X, Y):
    """
    Renvoie la distance moyenne de la particule à sa position initiale
    ainsi que la distance maximale atteinte par rapport à celle-ci.

    X et Y sont les listes contenant respectivement les abscisses et ordonnées
    des collisions d'une simulation.
    """
    d_max = 0
    S = 0  # somme des distances à la pos init
    for i in range(1, len(X)):
        d = math.sqrt(X[i]**2 + Y[i]**2)
        if d > d_max:
            d_max = d
        S += d
    return S / (len(X) - 1), d_max


def distances(LX, LY):
    """
    Renvoie la liste des distances moyennes à la posotion initiale de chacune
    des simulations ainsi que la liste des distances maximales atteintes.

    LX est une liste contenant les listes des abscisses des collisions de
    chaque simulation.
    LY est une liste contenant les listes des ordonnées des collisions de
    chaque simulation.
    """
    DMOY = []
    DMAX = []
    for i in range(len(LX)):
        d_moy, d_max = distance(LX[i], LY[i])
        DMOY.append(d_moy)
        DMAX.append(d_max)
    return DMOY, DMAX


def nb_collisions(LX, LY):
    """
    Renvoie une liste contenant le nombre total de collisions à chaque
    simulation.

    LX est une liste contenant les listes des abscisses des collisions de
    chaque simulation.
    LY est une liste contenant les listes des ordonnées des collisions de
    chaque simulation.
    """
    N = []
    for i in range(len(LX)):
        N.append(len(LX[i]))
    return N


def stats(LX, LY, boxes=False, verbose=False):
    """
    Renvoie des statistiques descriptives sur les variables lpm, distance
    moyenne et distance maximale.

    LX est une liste contenant les listes des abscisses des collisions de
    chaque simulation.
    LY est une liste contenant les listes des ordonnées des collisions de
    chaque simulation.
    """
    LPM = lpms(LX, LY)
    DMOY, DMAX = distances(LX, LY)
    Nb = nb_collisions(LX, LY)
    df = pd.DataFrame({"lpm": LPM, "Distance moyenne": DMOY,
                      "Distance maximale": DMAX, "Nombre de collisions": Nb})
    stats_des = df.describe()
    if verbose:
        print(stats_des)
    if boxes:
        df.boxplot(column=["lpm", "Distance moyenne", "Distance maximale"])
        plt.show()
    return df, stats_des
