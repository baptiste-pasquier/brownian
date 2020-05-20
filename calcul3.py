import multiprocessing
import pandas as pd
import time as tm
import psutil

from main import Simulation2, stats, NoBigLittleCollision, OutsideEnv

n = 4

c = Simulation2(nb_etapes=50, density=0.5, epsilon_time=0.02, dim=180, speed=10, speed_BP_init=10)


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

    df = pd.DataFrame(resul, columns=["Fréquence moyenne", "Distance moyenne", "Distance max"])

    print("\n#####################  Modèle n°3  #####################\n")
    print("NoBigLittleCollision :", No_big_little_collision)
    print("OutsideEnv :", Outside_env, "\n")
    print(df.describe())
    print("\nTemps d'exécution :", tm.time() - temps1)
