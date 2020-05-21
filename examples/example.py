from brownian.simulation1 import Simulation1
from brownian.simulation1_1 import BrownianMotion1_1
from brownian.simulation2 import Simulation2
from brownian.simulation3 import Simulation3
from brownian.outils import stats
from brownian.outils1_1 import statsSimulation

# Initialisation d'une simulation de type 1
a = Simulation1(nb_etapes=25, density=0.02, epsilon_time=0.5, time_interval=2, speed=10, speed_BP_init=10)
# Calcul de la simulation
a.calcul(show=True, coeff_affichage=2, pause=0.75)
# Affichage des statistiques
stats(a, show=True)
# Affichage de la trajectoire finale
a.traj_image(coeff_affichage=2)

# Idem avec une simulation de type 1.1
a1 = BrownianMotion1_1(epsilon=10**-4, n_etoile=10**4, v=10, V=1, h=10**-2)
# Affichage animé d'une simulation à 100 étapes
a1.simulationAnimated(100)
# Calculs d'une simulations à 100 étapes et affichage des statistiques
X, Y = a1.simulation(100)
statsSimulation(X, Y, verbose=True)

# Idem avec une simulation de type 2
b = Simulation2(nb_etapes=25, density=0.01, epsilon_time=0.5, dim=150, speed=10, speed_BP_init=10)
b.calcul(show=True, vector=False, pause=0.75)
stats(b, show=True)
b.traj_image()


# Idem avec une simulation de type 3
c = Simulation3(nb_etapes=5, density=0.01, epsilon_time=1, dim=100, speed=10, speed_BP_init=10, limit_collision_zone=10)
c.calcul(show=True, vector=False, pause=0.1)
stats(c, show=True)
c.traj_image()
