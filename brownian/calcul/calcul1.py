import multiprocessing
import pandas as pd
import time as tm
import numpy as np
import psutil

from simulations.simulation1 import Simulation1
from simulations.outils import stats

n = 16

a = Simulation1(nb_etapes=50, density=0.5, epsilon_time=0.02, time_interval=4, speed=10, speed_BP_init=10)


def f(i):
    a.calcul()
    return a.nb_no_collision, stats(a)


if __name__ == '__main__':

    nb_process = psutil.cpu_count(logical=False)
    print("Nombre de coeurs physiques : ", nb_process)
    temps1 = tm.time()

    pool = multiprocessing.Pool(processes=nb_process)
    pool_outputs = pool.map(f, [1] * n)
    pool.close()
    pool.join()
    resul = pool_outputs

    nb_no_collision = np.sum([elem[0] for elem in resul])

    mesures = [elem[1] for elem in resul]

    df = pd.DataFrame(mesures, columns=["Fréquence moyenne", "Distance moyenne", "Distance max"])

    print("\n#####################  Modèle n°1  #####################\n")
    print("NoBigCollision :", nb_no_collision, "\n")
    print(df.describe())
    print("\nTemps d'exécution :", tm.time() - temps1)
