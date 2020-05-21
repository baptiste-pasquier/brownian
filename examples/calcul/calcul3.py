import multiprocessing
import pandas as pd
import time as tm
import psutil

from brownian.simulation3 import Simulation3, NoBigLittleCollision
from brownian.simulation2 import OutsideEnv
from brownian.outils import stats 

n = 16

c = Simulation3(nb_max_collisions=5, density=10**4, epsilon_time=10**(-3), dim=0.05, speed=10, speed_BP_init=1)


def f(i):
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
    temps1 = tm.time()

    pool = multiprocessing.Pool(processes=nb_process)
    pool_outputs = pool.map(f, [1] * n)
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

    df = pd.DataFrame(resul, columns=["Fréquence", "lpm", "Distance moyenne", "Distance max", "Nb collisions"])

    print("\n#####################  Modèle n°3  #####################\n")
    print("NoBigLittleCollision :", No_big_little_collision)
    print("OutsideEnv :", Outside_env, "\n")
    print(df.describe())
    print("\nTemps d'exécution :", tm.time() - temps1)
