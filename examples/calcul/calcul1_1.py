import multiprocessing
import time as tm
import psutil

from brownian.simulation1_1 import BrownianMotion1_1
from brownian.outils1_1 import statsSimulations

n = 16
MVT = BrownianMotion1_1(epsilon=10**-4, n_etoile=10**4, v=10, V=0.1, h=10**-3)


def f(i):
    X, Y = MVT.simulation(1000)
    return X, Y


if __name__ == '__main__':

    nb_process = psutil.cpu_count(logical=False)
    print("Nombre de coeurs physiques : ", nb_process)
    temps1 = tm.time()

    pool = multiprocessing.Pool(processes=nb_process)
    pool_outputs = pool.map(f, [1] * n)
    pool.close()
    pool.join()
    resul = pool_outputs

    LX = [elem[0] for elem in resul]
    LY = [elem[1] for elem in resul]

    df, stats_des = statsSimulations(LX, LY)

    print("\n#####################  Modèle n°1.1  #####################\n")
    print(stats_des)
    print("\nTemps d'exécution :", tm.time() - temps1)
