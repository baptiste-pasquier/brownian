from random import uniform
import matplotlib.pyplot as plt
from math import cos, sin, pi, sqrt
import random

N = 5000

# --------------------------------- Méthode 1 -------------------------------- #

X = [uniform(-10, 10) for i in range(N)]
Y = [uniform(-10, 10) for i in range(N)]
plt.scatter(X, Y, s=1)
plt.show()


# --------------------------------- Méthode 2 -------------------------------- #

R = [uniform(0, 10) for i in range(N)]
Theta = [uniform(0, 2 * pi) for i in range(N)]
X = [R[i] * cos(Theta[i]) for i in range(N)]
Y = [R[i] * sin(Theta[i]) for i in range(N)]
plt.scatter(X, Y, s=1)
plt.show()


# --------------------------------- Méthode 3 -------------------------------- #

X = []
Y = []
while len(X) < N:
    x = uniform(-10, 10)
    y = uniform(-10, 10)
    if sqrt(x**2 + y**2) < 10:
        X.append(x)
        Y.append(y)
plt.scatter(X, Y, s=1)
plt.show()


# --------------------------------- Méthode 4 -------------------------------- #

X = []
Y = []
for i in range(N):
    r = uniform(0, 10)
    x2 = uniform(0, r**2)
    y2 = r**2 - x2
    X.append(random.choice([-1, 1]) * sqrt(x2))
    Y.append(random.choice([-1, 1]) * sqrt(y2))
plt.scatter(X, Y, s=1)
plt.show()


# --------------------------------- Méthode 5 -------------------------------- #

X = []
Y = []
for i in range(N):
    r = uniform(0, 1)
    theta = uniform(0, 2 * pi)
    X.append(10 * sqrt(r) * cos(theta))
    Y.append(10 * sqrt(r) * sin(theta))
plt.scatter(X, Y, s=1)
plt.show()
