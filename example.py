from main import Simulation1, Simulation2, Simulation3, stats

a = Simulation1(nb_etapes=25, density=0.02, epsilon_time=0.5, time_interval=2, speed=10, speed_BP_init=10)
a.calcul(show=True, coeff_affichage=2, pause=0.75)
stats(a, show=True)
a.traj_image(coeff_affichage=2)

b = Simulation2(nb_etapes=25, density=0.01, epsilon_time=0.5, dim=150, speed=10, speed_BP_init=10)
b.calcul(show=True, vector=False, pause=0.75)
stats(b, show=True)
b.traj_image()

# c = Simulation3(nb_etapes=5, density=0.01, epsilon_time=1, dim=100, speed=10, speed_BP_init=10, limit_collision_zone=10)
# c.calcul(show=True, vector=False, pause=0.1)
# stats(c, show=True)
# c.traj_image()


# c = Simulation3(nb_etapes=2, density=0.1, epsilon_time=0.05, dim=30, speed=10, speed_BP_init=10, limit_collision_zone=100)
# c.calcul()
# stats(c, show=True)
# c.traj_image()
