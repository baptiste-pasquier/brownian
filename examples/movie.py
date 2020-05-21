from brownian.simulation2 import Simulation2

b = Simulation2(nb_max_collisions=10, density=0.02, epsilon_time=0.25, dim=100, speed=10, speed_BP_init=10)
b.calcul(movie=True)
b.traj_image()
b.movie(coeff_affichage=1)
