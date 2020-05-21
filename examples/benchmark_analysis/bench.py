"""
L'execution de ce fichier fournit les données nécessaires pour comparer les modèles.
Les données sont enregistrées par défaut dans un fichier ~/Documents/resultats.pkl.
"""

import multiprocessing
import pandas as pd
import time as tm
import numpy as np
import psutil

from simulation1 import Simulation1
from outils import stats
from simulation1_1 import BrownianMotion1_1
from outils1_1 import statsSimulations
from simulation2 import Simulation2, NoBigCollision, OutsideEnv
from simulation3 import Simulation3, NoBigLittleCollision

N = 32
DUREE = 1


a = Simulation1(duree=DUREE, density=10**4, epsilon_time=10**-4, time_interval=10**-2, speed=10, speed_BP_init=0.1)

a1 = BrownianMotion1_1(epsilon=10**-4, n_etoile=10**4, v=10, V=0.1, h=10**-3)

b = Simulation2(duree=DUREE, density=10**4, epsilon_time=10**-4, dim=2, speed=10, speed_BP_init=0.1)

c = Simulation3(duree=DUREE, density=10**4, epsilon_time=10**-4, dim=0.05, speed=10, speed_BP_init=0.1)


def modele1(i):
    a.calcul()
    return a.nb_no_collision, stats(a)

def modele1_1(i):
    X, Y = a1.simulation(1024)
    return X, Y

def modele2(i):
    try:
        b.calcul()
    except NoBigCollision:
        return 1
    except OutsideEnv:
        return 2
    return stats(b)

def modele3(i):
    try:
        c.calcul()
    except NoBigLittleCollision:
        return 1
    except OutsideEnv:
        return 2
    return stats(c)


if __name__ == '__main__':

    nb_process = psutil.cpu_count(logical=False)
    print("Nombre de coeurs physiques : ", nb_process)
    
    pool = multiprocessing.Pool(processes=nb_process)
    temps1 = tm.time()
    pool_outputs = pool.map(modele1, [1] * N)
    pool.close()
    pool.join()
    resul = pool_outputs
    nb_no_collision = np.sum([elem[0] for elem in resul])
    mesures = [elem[1][1:] for elem in resul]
    df1 = pd.DataFrame(mesures, columns=["lpm", "Distance moyenne", "Distance max", "Nb collisions"])
    df1["Modèle"] = ["1"] * N
    print("\n#####################  Modèle n°1  #####################\n")
    print("NoBigCollision :", nb_no_collision, "\n")
    print(df1.describe())
    print("\nTemps d'exécution :", tm.time() - temps1)

    temps1_1 = tm.time()
    pool = multiprocessing.Pool(processes=nb_process)
    pool_outputs = pool.map(modele1_1, [1] * N)
    pool.close()
    pool.join()
    resul = pool_outputs
    LX = [elem[0] for elem in resul]
    LY = [elem[1] for elem in resul]
    df1_1 = statsSimulations(LX, LY)
    df1_1["Modèle"] = ["1.1"] * N
    print("\n#####################  Modèle n°1.1  #####################\n")
    print(df1_1.describe())
    print("\nTemps d'exécution :", tm.time() - temps1_1)

    temps2 = tm.time()
    pool = multiprocessing.Pool(processes=nb_process)
    pool_outputs = pool.map(modele2, [1] * N)
    pool.close()
    pool.join()
    resul = pool_outputs
    No_big_collision = resul.count(1)
    Outside_env = resul.count(2)
    while True:
        try:
            resul.remove(1)
        except ValueError:
            break
    while True:
        try:
            resul.remove(2)
        except ValueError:
            break
    res = [elem[1:] for elem in resul]
    df2 = pd.DataFrame(res, columns=["lpm", "Distance moyenne", "Distance max", "Nb collisions"])
    df2["Modèle"] = ["2"] * N
    print("\n#####################  Modèle n°2  #####################\n")
    print("NoBigCollision :", No_big_collision)
    print("OutsideEnv :", Outside_env, "\n")
    print(df2.describe())
    print("\nTemps d'exécution :", tm.time() - temps2)

    temps3 = tm.time()
    pool = multiprocessing.Pool(processes=nb_process)
    pool_outputs = pool.map(modele3, [1] * N)
    pool.close()
    pool.join()
    resul = pool_outputs
    No_big_little_collision = resul.count(1)
    Outside_env = resul.count(2)
    while True:
        try:
            resul.remove(1)
        except ValueError:
            break
    while True:
        try:
            resul.remove(2)
        except ValueError:
            break
    res = [elem[1:] for elem in resul]
    df3 = pd.DataFrame(res, columns=["lpm", "Distance moyenne", "Distance max", "Nb collisions"])
    df3["Modèle"] = ["3"] * N
    print("\n#####################  Modèle n°3  #####################\n")
    print("NoBigLittleCollision :", No_big_little_collision)
    print("OutsideEnv :", Outside_env, "\n")
    print(df3.describe())
    print("\nTemps d'exécution :", tm.time() - temps3)

    print("\n")
    result = pd.concat([df1, df1_1, df2, df3])
    print(result)

    result.to_pickle("~/Documents/resultats.pkl") 
